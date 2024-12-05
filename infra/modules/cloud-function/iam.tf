# Compte de service storage agent necessaire pour GCS CloudEvent triggers
data "google_storage_project_service_account" "default" {
  project = var.project_id
}

resource "google_project_iam_member" "gcs_pubsub_publishing" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${data.google_storage_project_service_account.default.email_address}"
}

# Permissions au  service account utilisée par la cloud function et  Eventarc trigger
resource "google_project_iam_member" "invoking" {
  project    = var.project_id
  role       = "roles/run.invoker"
  member     = "serviceAccount:${var.service_account_email}"
  depends_on = [google_project_iam_member.gcs_pubsub_publishing]
}


resource "google_project_iam_member" "event_receiving" {
  project    = var.project_id
  role       = "roles/eventarc.eventReceiver"
  member     = "serviceAccount:${var.service_account_email}"
  depends_on = [google_project_iam_member.invoking]
}

resource "google_project_iam_member" "artifactregistry_reader" {
  project    = var.project_id
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${var.service_account_email}"
  depends_on = [google_project_iam_member.event_receiving]
}

# Permissions Google BigQuery au  service account utilisée par la cloud function
resource "google_project_iam_member" "bigquery_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${var.service_account_email}"
}

resource "google_project_iam_member" "bigquery_iam_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${var.service_account_email}"
}

# Permissions Google Storage au  service account utilisée par la cloud function
resource "google_project_iam_member" "storage_admin_sa" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${var.service_account_email}"
}
# Dans modules/cloud-function/iam.tf
resource "google_service_account_iam_member" "terraform_sa_user" {
  service_account_id = "projects/${var.project_id}/serviceAccounts/${var.service_account_email}"
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:terraform-sa@e-datacap.iam.gserviceaccount.com"
}