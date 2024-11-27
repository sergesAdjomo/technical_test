# validation de l'existence du project_id
data "google_project" "project" {
  project_id = var.project_id
}

# Creation du service account
resource "google_service_account" "gcf_service_account" {
  project                      = data.google_project.project.project_id
  account_id                   = var.service_account_name
  create_ignore_already_exists = true
}

# Module pour la création du bucket GCS pour stocker les fichiers de données
module "data_input_bucket" {
  source      = "./modules/cloud-storage"
  project_id  = data.google_project.project.project_id
  location    = var.region
  bucket_name = var.data_input_bucket_name
  create_bucket = true  # Ne pas créer le bucket si déjà existant
}

# Module pour la création du bucket GCS pour les schémas
module "schema_bucket" {
  source      = "./modules/cloud-storage"
  project_id  = data.google_project.project.project_id
  location    = var.region
  bucket_name = "${var.project_id}-schemas"
  create_bucket = true  # Ne pas créer le bucket si déjà existant
}

# Module pour la création du bucket GCS pour stocker les fichiers source de la fonction Cloud
module "gcs_bucket_gcf_source" {
  source      = "./modules/cloud-storage"
  project_id  = data.google_project.project.project_id
  location    = var.region
  bucket_name = var.gcs_bucket_name
}

locals {
  schema_files = fileset("${path.module}/tables_schema", "*.json")
}

# Upload chaque fichier de schéma vers GCS
resource "google_storage_bucket_object" "schema_files" {
  for_each = local.schema_files
  
  name   = "${each.value}"
  source = "${path.module}/tables_schema/${each.value}"
  bucket = module.schema_bucket.bucket_name
  
  content_type = "application/json"
}

# Module pour la création du dataset BigQuery
module "bigquery_dataset" {
  source     = "./modules/bigquery-dataset"
  project_id = data.google_project.project.project_id
  dataset_id = var.dataset_id
  location   = var.region
}

# Module pour le bucket des sources de Cloud Function
module "cloud_function_source_bucket" {
  source      = "./modules/cloud-storage"
  project_id  = data.google_project.project.project_id
  location    = var.region
  bucket_name = var.gcs_bucket_name
  create_bucket = false   # Ne pas créer le bucket si déjà existant
}

# Module pour la création de la Cloud Function v2
module "cloud_function" {
  source                = "./modules/cloud-function"
  for_each             = { for gcf in var.cloud_functions : gcf.function_name => gcf }
  project_id           = data.google_project.project.project_id
  region               = var.region
  function_name        = each.value.function_name
  function_bucket_name = module.cloud_function_source_bucket.bucket_name
  data_input_bucket    = module.data_input_bucket.bucket_name
  dataset_id           = module.bigquery_dataset.dataset_id
  entry_point          = each.value.entry_point
  function_source_path = each.value.source_path
  service_account_email = google_service_account.gcf_service_account.email
  schema_bucket_name    = module.schema_bucket.bucket_name
}

# Artifacts Registry
resource "google_artifact_registry_repository" "mt-test-repo" {
  project       = data.google_project.project.project_id
  location      = var.region
  repository_id = "mt-test-repo"
  description   = "opportunity_manager docker repository"
  format        = "DOCKER"
}