resource "google_storage_bucket" "etl_bucket" {
  count = var.create_bucket ? 1 : 0  # Créer le bucket si la variable create_bucket est vraie
  name          = var.bucket_name # Nom du bucket passé en variable
  location      = var.location    # Localisation du bucket
  project       = var.project_id  # Projet GCP
  storage_class = "STANDARD"      # Classe de stockage du bucket
  force_destroy = true            # Permet de détruire le bucket même s'il contient des objets

  #   prevent_destroy = true   # Prevent Terraform from destroying the bucket
  # ne plus creer si le bucket existe déjà
  lifecycle {
    prevent_destroy = true
  }

  depends_on = [
    google_storage_bucket.etl_bucket
  ]

}
