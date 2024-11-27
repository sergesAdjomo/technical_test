import logging
import os
from typing import Dict
from typing import List
import json
import functions_framework
import jq
import ndjson
from google.cloud import bigquery
from google.cloud import storage


@functions_framework.cloud_event
def load_data(cloud_event):
    try:
        data: Dict = cloud_event.data
        # Set up BigQuery client
        client = bigquery.Client()
        storage_client = storage.Client()
        dataset_ref = f"{os.environ.get('PROJECT_ID')}.{os.environ.get('DATASET_ID')}"
        bucket_name = data['bucket']
        source_file = str(data["name"])
        file_extension = source_file.split('.')[1]
        table_ref = f"{os.environ.get('PROJECT_ID')}.{os.environ.get('DATASET_ID')}.{source_file.split('.')[0]}"

        # load a schema file.
        schema = [bigquery.SchemaField(name=x.get('name'), field_type=x.get('type'), mode=x.get('mode'),
                                       description=x.get('description'))
                  for x in read_json_file(storage_client,
                                          os.environ.get('BUCKET_NAME'),
                                          f"{source_file.split('.')[0]}.json")
                  ]

        # Ingest file based on the file extension
        match file_extension:
            case "csv":
                print(f"{file_extension} is the extension of the file.")
                job_config = bigquery.LoadJobConfig(
                    source_format=bigquery.SourceFormat.CSV,
                    skip_leading_rows=1,
                    autodetect=True, schema=schema)
                load_job = client.load_table_from_uri(f"gs://{bucket_name}/{source_file}", table_ref,
                                                      job_config=job_config)  # Make an API request.
            case "json":
                print(f"{file_extension} is the extension of the file.")
                job_config = bigquery.LoadJobConfig(
                    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                    schema=schema,
                    autodetect=False)
                load_job = client.load_table_from_uri(f"gs://{bucket_name}/{source_file}", table_ref,
                                                      job_config=job_config)  # Make an API request.
            case _:
                print("Not yet implemented")

        load_job.result()  # Waits for the job to complete.
        destination_table = client.get_table(table_ref)  # Make an API request.
        print(f"Loaded {source_file} into {dataset_ref}.{table_ref}")
        print("Loaded {} rows.".format(destination_table.num_rows))

    except Exception as ex:
        logging.error(f"Error loading {source_file}: {ex}")
        raise ex


def read_json_file(storage_client, bucket_name: str, filename: str):
    bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.get_blob(filename)

    json_data_string = blob.download_as_string()

    # Convert the json lines String to a List of Dict
    json_data_as_dicts: List[Dict] = json.loads(json_data_string)

    return json_data_as_dicts
