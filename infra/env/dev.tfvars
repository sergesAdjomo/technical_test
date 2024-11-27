project_id              = "e-datacap"                             # ID du projet GCP
region                  = "us-central1"
gcs_bucket_name         = "gcf-source-001"                       # Bucket pour le code source de la Cloud Function
data_input_bucket_name  = "data-files-01"                       # Bucket pour les fichiers de données
schema_bucket_name      = "e-datacap-schemas"                   # Bucket pour les schémas
dataset_id             = "ds_etl"                               # ID du dataset BigQuery
cloud_functions = [{
  function_name = "load_file_to_bq"                            # Nom de la Cloud Function
  entry_point   = "load_data"                                  # Nom de la fonction à exécuter
  source_path   = "src/cloud_function/00_load_file_to_bq"      # Chemin relatif du code source
}]
service_account_name    = "gcf-sa"                            # Nom du service account