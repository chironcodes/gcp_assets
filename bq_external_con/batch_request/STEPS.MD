
```sh
CREATE OR REPLACE FUNCTION {{DATASET_ID}}.{{FUNCTION_NAME}}(id INT64) RETURNS JSON
REMOTE WITH CONNECTION `{{PROJECT_ID}}.us.my-cats-con`
    OPTIONS (
        -- change this to reflect the Trigger URL of your cloud function (look for the TRIGGER tab)
        endpoint = 'https://{{REGION}}-{{PROJECT_ID}}.cloudfunctions.net/cat_router'
    )

SELECT
    start_station_id, end_station_id, 
    blogs.add_fake_user(trip_id, bikeid)
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
LIMIT 10


```


## Sample payload
```json
{
    "calls": [
        [
            1
        ],
        [
            2
        ],
        [
            3
        ]
    ]
}

```

## Sample usage on BQ
```sql
WITH random_data_cte AS (
    SELECT
        CAST(ROW_NUMBER() OVER () AS INT64) AS id,
        CAST(CONCAT('Name', RAND()) AS STRING) AS name
    FROM UNNEST(GENERATE_ARRAY(1, 3))
),
cte AS (
    SELECT 
        id,
        {{DATASET_ID}}.{{FUNCTION_NAME}}(id) as reply,
        name
    FROM random_data_cte
)
SELECT 
    * EXCEPT(reply),
    JSON_EXTRACT_SCALAR(reply, '$.id') AS id,
    JSON_EXTRACT_SCALAR(reply, '$.cat_fact') AS cat_fact
FROM cte

```
