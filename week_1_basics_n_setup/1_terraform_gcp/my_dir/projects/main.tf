terraform {
  backend "local" {}
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file("/home/romasl/Documents/LEARN/DE/DEZOOMCAMP23/week_1_basics_n_setup/1_terraform_gcp/my_dir/dtc-de-course-384415-46a806037535.json")

  project = var.project # 
  region  = var.region # "europe-west4"
}

resource "google_storage_bucket" "data_lake_bucket" {
  name = "${local.data_lake_bucket}_${var.project}"
  location = var.region

  storage_class = var.storage_class
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }
  force_destroy = true
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project = var.project
  location = var.region
  
}

