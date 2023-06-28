# Uncomment the line below only if you intend to test locally
# import functions_framework
# functions-framework --target gmaps_batch_api --debug

import os
import json
import requests
import concurrent.futures

from google.oauth2 import service_account
import googlemaps

api_key = "AIzDUmmLEap6xbd5RDr-Bw4JW2GDgSyBekJAS3U"
gmaps = googlemaps.Client(api_key)

# define the max number of threads
max_workers = 100

def send_single_request(address):

    try:
        result = gmaps.find_place(
            address,
            "textquery",
            fields=[
                "formatted_address",
                "business_status",
                "types",
                "geometry/location/lat",
                "geometry/location/lng",
                "place_id",
                "plus_code",
                "user_ratings_total",
            ],
            language="en-US",
        )
        return result
    except Exception as e:
        print(f"Error searching for place: {e}")
        return None


def gmaps_batch_api(request):

    try:
        payload = request.get_json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

    if payload.get("calls"):
        calls = payload["calls"]
    else:
        return json.dumps({'error': 'Invalid request payload'}), 500

    # Create a ThreadPoolExecutor

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_single_request, call[0]) for call in calls]

    # Wait for all tasks to complete
    print("Waiting task finish")
    concurrent.futures.wait(futures)

    # Retrieve the results
    results = [json.loads(future.result()) for future in futures]

    print(results)
    return_json = json.dumps({"replies":  results})

    return return_json
