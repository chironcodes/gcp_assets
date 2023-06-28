# Uncomment the line below only if you intend to test locally
# import functions_framework
# functions-framework --target single_cat_request --debug

import os
import json
import requests

from google.oauth2 import service_account



def single_cat_request(request):

    try:
        payload = request.get_json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

    
    if payload.get("id"):
        id= payload["id"]
    else:
        return json.dumps({'error':'Invalid request payload'}),500
    
    try:
        response = requests.get(f'https://meowfacts.herokuapp.com/?id={id}')
        if response.status_code==200:
            data = response.json()['data']
            answer={
                'input': id,
                'output': data[0]
            }
        else:
            answer={
                'input': id,
                'output': ''
            }
    except Exception as err:
        answer={
            'input': id,
            'output': ''
            }
        print(f"Unexpected {err=}, {type(err)=}")
    return_json = json.dumps(answer)
    
    return return_json