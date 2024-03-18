import azure.functions as func
import requests
import logging
import os
from urllib.parse import urlencode

AUTHORIZE_URL = 'https://www.inaturalist.org/oauth/authorize'
TOKEN_URL = 'https://www.inaturalist.org/oauth/token'
CREATE_OFV_URL = 'https://api.inaturalist.org/v1/observation_field_values'

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def get_authorization_code_url():
    params = {
        'client_id': os.environ["CLIENT_ID"],
        'redirect_uri': os.environ["REDIRECT_URI"],
        'response_type': 'code'
    }
    return AUTHORIZE_URL + '?' + urlencode(params)

@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def whatever(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. Open {get_authorization_code_url()}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    
def get_access_token(authorization_code):
    data = {
        'client_id': os.environ["CLIENT_ID"],
        'client_secret': os.environ["CLIENT_SECRET"],
        'code': authorization_code,
        'redirect_uri': os.environ["REDIRECT_URI"],
        'grant_type': 'authorization_code'
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None    

@app.route(route="update", auth_level=func.AuthLevel.ANONYMOUS)
def update(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    code = req.params.get('auth-code')
    observation_id = req.params.get('state')

    if code:
        data = {
            "observation_field_value": {
                "observation_id": observation_id,
                "observation_field_id": 42,
                "value": "n/a"
            }
        }
        api_call_headers = {'Authorization': 'Bearer ' + get_access_token(code)}
        response = requests.post(CREATE_OFV_URL, json=data, headers=api_call_headers)
        return func.HttpResponse(f"Yay! The iNaturalist observation was updated {response}!")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

# @app.route(route="update_inaturalist")
# def update_inaturalist(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python update function processed a request.')

#     code = req.params.get('code')

#     if code:
#         return func.HttpResponse(f"Hello, {code}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a code in the query string for a personalized response.",
#              status_code=401
#         )    