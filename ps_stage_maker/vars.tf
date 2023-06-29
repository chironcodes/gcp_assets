
##################################################
# labels  Configuration                          #
##################################################

variable "resource_labels" {
  type = map(string)
  default = {
    environment = "dev", ## @@@@@
    squad       = "business_analytics"
  }
}

##################################################
# General  Configuration                         #
##################################################


variable "project_id" {
  type        = string
  default     = "your-projectd-dev" ## @@@@@
  description = "The default GCP project."
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "The default region to be used on GCP."
}

variable "zone" {
  type        = string
  default     = "us-central1-c"
  description = "The default zone to be used on GCP."
}

##################################################
# BigQuery Configuration                         #
##################################################

variable "dataset_id" {
  type        = string
  default     = "raw_pubsub"
  description = "The default Dataset id to be used to store raw subscription."
}


##################################################
# Pub/Sub Configuration                         #
##################################################


variable "ack_deadline_seconds" {
  type        = number
  default     = 600
  description = "The default ack deadline to be used by your subscription."
}
