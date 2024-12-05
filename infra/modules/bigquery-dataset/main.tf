# Création du dataset BigQuery
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.dataset_id # ID du dataset passé en variable
  project    = var.project_id # Projet GCP
  location   = var.location   # Localisation du dataset

  lifecycle {
    prevent_destroy = true # Prevent Terraform from destroying the dataset
  }
}
