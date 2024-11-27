variable "project_id" {
  description = "ID du projet GCP"
  type        = string
}

variable "region" {
  description = "Région de déploiement"
  type        = string
}

variable "function_name" {
  description = "Nom de la Cloud Function"
  type        = string
}

variable "service_account_email" {
  description = "Service Account de la Cloud Function"
  type        = string
}

variable "data_input_bucket" {
  description = "Bucket GCS pour déclencher la Cloud Function"
  type        = string
}

variable "function_bucket_name" {
  description = "Le nom du bucket GCS qui stocke le code source de la Cloud Function"
  type        = string
}

variable "function_source_path" {
  description = "Chemin vers le code source "
  type        = string
}

variable "entry_point" {
  description = "Cloud function entry point "
  type        = string
}

variable "dataset_id" {
  description = "ID of the BigQuery dataset."
  type        = string
}

variable "schema_bucket_name" {
  description = "Nom du bucket contenant les schémas"
  type        = string
}