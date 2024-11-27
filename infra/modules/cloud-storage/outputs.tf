# Sortie de la ressource google_storage_bucket
output "bucket_name" {
  description = "The name of the created GCS bucket."
  value       = var.create_bucket ? (length(google_storage_bucket.etl_bucket) > 0 ? google_storage_bucket.etl_bucket[0].name : var.bucket_name) : var.bucket_name
}
