variable "dataset_id" {
  description = "ID of the BigQuery dataset."
  type        = string
}

variable "location" {
  description = "Location for BigQuery dataset and table."
  type        = string
}

variable "project_id" {
  description = "The project ID for BigQuery resources."
  type        = string
}
