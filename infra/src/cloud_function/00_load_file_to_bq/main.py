import logging
import os
from typing import Dict, List
import json
import functions_framework
from google.cloud import bigquery
from google.cloud import storage

@functions_framework.cloud_event
def load_data(cloud_event):
    try:
        data: Dict = cloud_event.data
        logging.info(f"Event received: {json.dumps(data)}")
        
        client = bigquery.Client()
        storage_client = storage.Client()
        
        # Extraire les informations du fichier
        bucket_name = data['bucket']
        source_file = str(data["name"]).lower()
        file_name_without_ext = os.path.splitext(source_file)[0]
        file_extension = os.path.splitext(source_file)[1].lstrip('.')
        
        logging.info(f"File details - Bucket: {bucket_name}, File: {source_file}")
        logging.info(f"File parsed - Name: {file_name_without_ext}, Extension: {file_extension}")
        
        # Construire les références
        project_id = os.environ.get('PROJECT_ID')
        dataset_id = os.environ.get('DATASET_ID')
        dataset_ref = f"{project_id}.{dataset_id}"
        table_ref = f"{dataset_ref}.{file_name_without_ext}"
        
        logging.info(f"Project Configuration - Project: {project_id}, Dataset: {dataset_id}")
        logging.info(f"Table Reference: {table_ref}")
        
        schema_bucket = os.environ.get('BUCKET_NAME')
        schema_file = f"{file_name_without_ext}.json"
        logging.info(f"Looking for schema in bucket {schema_bucket}: {schema_file}")

        try:
            schema = [
                bigquery.SchemaField(
                    name=x.get('name'),
                    field_type=x.get('type'),
                    mode=x.get('mode', 'NULLABLE'),
                    description=x.get('description', '')
                )
                for x in read_json_file(
                    storage_client,
                    schema_bucket,
                    schema_file
                )
            ]
            logging.info(f"Schema loaded successfully with {len(schema)} fields")
            logging.info(f"Schema details: {[{f.name: f.field_type} for f in schema]}")
        except Exception as schema_error:
            logging.error(f"Error loading schema: {schema_error}")
            raise schema_error

        # Configuration du job selon l'extension
        job_config = bigquery.LoadJobConfig(schema=schema, autodetect=False)
        
        if file_extension.lower() == "csv":
            logging.info("Configuring CSV load job")
            job_config.source_format = bigquery.SourceFormat.CSV
            job_config.skip_leading_rows = 1
        elif file_extension.lower() == "json":
            logging.info("Configuring JSON load job")
            job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")

        # Charger les données
        uri = f"gs://{bucket_name}/{source_file}"
        logging.info(f"Starting load job from {uri} to {table_ref}")
        load_job = client.load_table_from_uri(
            uri,
            table_ref,
            job_config=job_config
        )
        
        logging.info("Waiting for load job to complete...")
        load_job.result()  # Attendre la fin du job
        
        # Vérifier le résultat
        destination_table = client.get_table(table_ref)
        logging.info(f"Loaded {destination_table.num_rows} rows into {table_ref}")
        
        return f"Successfully loaded {source_file}"

    except Exception as ex:
        logging.error(f"Error processing {source_file}: {str(ex)}")
        raise

def read_json_file(storage_client, bucket_name: str, filename: str) -> List[Dict]:
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.get_blob(filename)
        
        if not blob:
            raise FileNotFoundError(f"Schema file not found: {filename}")
        
        json_data_string = blob.download_as_string().decode('utf-8')
        logging.info(f"Raw schema content for {filename}: {json_data_string[:200]}...")  # Log les 200 premiers caractères
        
        try:
            schema_data = json.loads(json_data_string)
            logging.info(f"Schema type: {type(schema_data)}")
            
            if isinstance(schema_data, str):
                # Si le schéma est une chaîne, essayons de le parser à nouveau
                schema_data = json.loads(schema_data)
            
            if not isinstance(schema_data, list):
                raise ValueError(f"Schema must be a list, got {type(schema_data)}")
            
            # Vérification de la structure de chaque élément
            for item in schema_data:
                if not isinstance(item, dict):
                    raise ValueError(f"Schema item must be a dictionary, got {type(item)}")
                if 'name' not in item or 'type' not in item:
                    raise ValueError(f"Missing required fields in schema item: {item}")
            
            return schema_data
            
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error in {filename}: {str(e)}")
            logging.error(f"Problematic content: {json_data_string}")
            raise
            
    except Exception as e:
        logging.error(f"Error reading schema file {filename}: {str(e)}")
        raise