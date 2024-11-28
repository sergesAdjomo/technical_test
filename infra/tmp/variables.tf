
variable "project_id" {
  description = "ID du projet Google Cloud"
  type        = string
  default     = "e-datacap"
}

variable "region" {
  description = "Région pour les ressources Google Cloud"
  type        = string
  default     = "us-central1"
}

variable "dataset_id" {
  description = "ID du dataset BigQuery"
  type        = string
}

variable "service_account_name" {
  description = "Service Account pour exécuter la Cloud Function"
  type        = string
}

variable "gcs_bucket_name" {
  description = "Le nom du bucket GCS qui stocke le code source de la Cloud Function"
  type        = string
}

variable "data_input_bucket_name" {
  description = "Nom du bucket GCS qui contient les fichiers de données"
  type        = string
}

# Ajout de la variable schema_bucket_name
variable "schema_bucket_name" {
  description = "Nom du bucket GCS qui contient les schémas"
  type        = string
}
variable "cloud_functions" {
  description = "liste des cloud functions à deployer"
  type = list(object({
    function_name = string,
    entry_point   = string
    source_path   = string
  }))

}

