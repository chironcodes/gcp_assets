from google.cloud import pubsub_v1


# TODO: fetch project_env as environment variable
env = "stg"
project_id = f"your-projectd-{env}"

# Instantiates a Pub/Sub client
client = pubsub_v1.PublisherClient()

# Lists all topics in the project
project_path = f"projects/{project_id}"

topics = ""
for topic in client.list_topics(request={"project": project_path}):
    if topic.name.__contains__(f"-{env}-"):
            if not topic.name.__contains__("dead"):
                topics += topic.name.split("topics/")[1] + "\n"

topics=topics[:-1]
with open("topics.txt", "a") as f:
    f.write(topics)


"""
gcloud config set project your-projectd-dev-dev
gcloud config set project your-projectd-dev-stg
gcloud config set project your-projectd-dev-prd


service-[projectid]@gcp-sa-pubsub.iam.gserviceaccount.com
om
terraform init
terraform apply -auto-approve
terraform destroy -auto-approve


terraform apply -parallelism=200 -auto-approve

terraform plan

terraform plan \
-out=create.plan


gcloud pubsub subscriptions list --format='value(name)' | grep /subscriptions/raw- | xargs -P 15 -n 1 gcloud pubsub subscriptions delete
"""