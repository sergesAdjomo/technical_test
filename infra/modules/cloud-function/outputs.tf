output "function_name" {
  value = google_cloudfunctions2_function.cloud_function.name
}

output "function_url" {
  description = "L'URL de la Cloud Function"
  value       = google_cloudfunctions2_function.cloud_function.service_config[0].uri
}
