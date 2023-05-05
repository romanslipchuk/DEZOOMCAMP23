locals {
  data_lake_bucket = "dtc_data_klake"
}

variable "project" {
  description = "dtc-de-course-384415"
  default = "dtc-de-course-384415"
}

variable "region" {
  description = "europe-west6"
  default = "europe-west6"
  type = string
}

variable "storage_class" {
  description = "I'll check what type is more preferrable when get to this"
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "Big Querry Dataset will contain raw data"
  type = string
  default = "trips_data_all"
}
