# terraform {
#  backend "gcs" {
#    bucket  = "your_bucket_name"
#    prefix  = "terraform/state/dev"
#  }
# }


terraform {
 backend "gcs" {
   bucket  = "your_bucket_name"
   prefix  = "terraform/state/stg"
 }
}


# terraform {
#  backend "gcs" {
#    bucket  = "your_bucket_name"
#    prefix  = "terraform/state/prd"
#  }
# }