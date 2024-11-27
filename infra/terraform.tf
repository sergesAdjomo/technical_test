terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.42.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "5.42.0"
    }
  }


  backend "gcs" {
    bucket = "edata-terraform-tfstate-files"
    prefix = "terraform/tfstate"
  }

  /* Uncomment this block to use Terraform Cloud for this tutorial
cloud {
  organization = "organization-name"
  workspaces {
    name = "learn-terraform-module-use"
  }
}
*/
}
