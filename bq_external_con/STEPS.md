## based on https://towardsdatascience.com/remote-functions-in-bigquery-af9921498438

## https://medium.com/google-cloud/how-to-create-remote-functions-in-bigquery-8a2319038308

gcloud services enable cloudfunctions.googleapis.com --async
gcloud services enable cloudbuild.googleapis.com --async
gcloud services enable bigqueryconnection.googleapis.com --async


```sh
bq mk --connection \
--display_name='my_cats_con' \
--connection_type=CLOUD_RESOURCE \
--project_id=$(gcloud config get-value project) \
--location=US  my-cats-con
```


```sh
    bq show --location=US --connection my-cats-con
```

## add service account, on permission tab, the invoke function access






```sh

```