# Archivage du code source de la cloud function
data "archive_file" "default" {
  type        = "zip"
  output_path = "${path.cwd}/tmp/${var.function_name}.zip"
  source_dir  = var.function_source_path
}

# Déclaration de l'objet GCS qui contient le fichier ZIP avec le code source de la fonction
resource "google_storage_bucket_object" "function_zip" {
  name       = "${data.archive_file.default.output_md5}.zip"
  bucket     = var.function_bucket_name
  source     = data.archive_file.default.output_path
  depends_on = [data.archive_file.default]
}

# Création de la fonction Cloud Gen2
resource "google_cloudfunctions2_function" "cloud_function" {
  name        = var.function_name
  project     = var.project_id
  location    = var.region
  description = "Cloud Function to load data into BigQuery from GCS files"

  build_config {
    runtime     = "python311"
    entry_point = var.entry_point
    source {
      storage_source {
        bucket = var.function_bucket_name
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    available_memory = "256M"
    timeout_seconds  = 60
    environment_variables = {
      PROJECT_ID  = var.project_id
      DATASET_ID  = var.dataset_id
      BUCKET_NAME = var.schema_bucket_name
    }
    ingress_settings               = "ALLOW_INTERNAL_ONLY"
    all_traffic_on_latest_revision = true
    service_account_email          = var.service_account_email
  }

  event_trigger {
    trigger_region        = var.region
    event_type            = "google.cloud.storage.object.v1.finalized"
    service_account_email = var.service_account_email
    retry_policy          = "RETRY_POLICY_RETRY"
    event_filters {
      attribute = "bucket"
      value     = var.data_input_bucket
    }
  }

  lifecycle {
    replace_triggered_by = [
      google_storage_bucket_object.function_zip
    ]
  }
}