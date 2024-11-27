variable "bucket_name" {
  description = "The name of the GCS bucket."
  type        = string
}

variable "location" {
  description = "The location of the GCS bucket."
  type        = string
}

variable "project_id" {
  description = "The project ID where the bucket will be created."
  type        = string
}

variable "create_bucket" {
  description = "Whether to create the bucket or not"
  type        = bool
  default     = true
}
