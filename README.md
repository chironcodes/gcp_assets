# gcp_assets




# activate gcloud sdk with service account file
gcloud auth activate-service-account --key-file=key.json



# bq_external_con


# ps_stage_maker
Since 29/06/2023, coincidently one year from now, Google has made it possible to dump data directly from pub/sub topics to a BigQuery table, eliminating the need for the (expensive) Dataflow for real-time ingestion.

This asset was created as part of a big FinOPS operation and helped reduce the client's cost by more than 35% just by retiring old n' good Dataflow.

How it works:
The code is clear and straightforward: 
    1. We use pub/sub import to list all existing topics within the project and apply some rules to define what was 'human-made'.
        ```python
            if topic.name.__contains__(f"-{env}-"):
                    if not topic.name.__contains__("dead"):
                        topics += topic.name.split("topics/")[1] + "\n"
        # In the project all human-made flows had 'env' in the string e.g ('geo-dev-xx','tracer-stg-local-xx').
        # We also had some deadletters topics with the same pattern 
        ```

        ```python
        topics=topics[:-1]
        with open("topics.txt", "a") as f:
            f.write(topics)
        # In the last code, you saw that we concatenated every topic with a '\n',
        #  to break the line every time; now we remove the last one and save it to our file
        ```

    2. On our terraform script we can the access this file and iterate over it 
        ```hcl

            locals {
        topic_names = split("\n", file("${path.module}/topics.txt"))
            }
        ```

    2.2 
        ```hcl
        ...
            table_id   = join("-", ["raw", each.value])
            # Later on, we can use the topic's name to create tables within a pattern e.g 
    "raw-",{{topic_name}}
        ...
    

    2.3
        ```hcl
        ...
        name = join("-", ["raw", each.value])
        # The same logic applied to our subscription's name

        ...

        ```

    You quickly migrated your entire stream workflow from the expensive GCP Dataflow for a scalable, managed and much cheaper solution.


    
