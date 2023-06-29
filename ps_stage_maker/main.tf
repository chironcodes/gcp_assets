# Define the provider
provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone

}

resource "random_id" "bucket_prefix" {
  byte_length = 8
}

resource "google_storage_bucket" "default" {
  name          = "${random_id.bucket_prefix.hex}-bucket-tfstate"
  force_destroy = false
  location      = "US"
  storage_class = "STANDARD"
  versioning {
    enabled = true
  }
}

locals {
  topic_names = split("\n", file("${path.module}/topics.txt"))
}


resource "google_bigquery_table" "table" {

  labels              = var.resource_labels
  deletion_protection = false

  for_each = { for topic_name in local.topic_names : topic_name => topic_name }

  dataset_id = var.dataset_id
  table_id   = join("-", ["raw", each.value])

  time_partitioning {
    type = "DAY"
  }

  schema = <<EOF
    [
    {
      "name": "subscription_name",
      "mode": "REQUIRED",
      "type": "STRING",
      "description": "Name of a subscription.",
      "fields": []
    },
    {
      "name": "message_id",
      "mode": "REQUIRED",
      "type": "STRING",
      "description": "ID of a message",
      "fields": []
    },
    {
      "name": "publish_time",
      "mode": "REQUIRED",
      "type": "TIMESTAMP",
      "description": "The time of publishing a message.",
      "fields": []
    },
    {
      "name": "data",
      "mode": "REQUIRED",
      "type": "STRING",
      "description": "The message body.",
      "fields": []
    },
    {
      "name": "attributes",
      "mode": "NULLABLE",
      "type": "JSON",
      "description": "A JSON object containing all message attributes. It also contains additional fields that are part of the Pub/Sub message including the ordering key, if present.",
      "fields": []
    }
    ]
    EOF

}


resource "google_pubsub_subscription" "my_subscription" {

  labels = var.resource_labels


  depends_on = [google_bigquery_table.table]
  for_each   = { for topic_name in local.topic_names : topic_name => topic_name }

  name = join("-", ["raw", each.value])

  topic = each.value

  bigquery_config {
    table          = "${var.project_id}.${var.dataset_id}.${join("-", ["raw", each.value])}"
    write_metadata = true
  }

  ack_deadline_seconds = var.ack_deadline_seconds
  expiration_policy {
    ttl = ""
  }
  retain_acked_messages   = false
  enable_message_ordering = false


}
