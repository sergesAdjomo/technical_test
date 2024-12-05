# Dans outputs.tf à la racine du projet

output "schema_files_uploaded" {
  value = {
    for file in google_storage_bucket_object.schema_files :
    file.name => "gs://${file.bucket}/${file.name}"
  }
  description = "Liste des schémas uploadés avec leurs URLs"
}

output "schema_files_count" {
  value       = length(google_storage_bucket_object.schema_files)
  description = "Nombre de fichiers de schéma uploadés"
}

output "bucket_details" {
  value = {
    cloud_function_source = module.cloud_function_source_bucket.bucket_name
    schemas               = module.schema_bucket.bucket_name
    data_input            = module.data_input_bucket.bucket_name
  }
  description = "Noms des différents buckets et leurs rôles"
}