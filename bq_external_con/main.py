# Uncomment the line below only if you intend to test locally
# import functions_framework
# functions-framework --target gmaps_batch_api --debug

import os
import json
import requests

from google.oauth2 import service_account



def send_single_request(body):
    body = {
        'address': body
    }
    response = requests.get(PROJECT_SINGLE_REQ_URL, json=body)
    return response.text

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
        futures = [executor.submit(send_request, call[0]) for call in calls]

    # Wait for all tasks to complete
    print("Waiting task finish")
    concurrent.futures.wait(futures)

    # Retrieve the results
    results = [json.loads(future.result()) for future in futures]

    print(results)
    return_json = json.dumps({"replies":  results})

    return return_json
