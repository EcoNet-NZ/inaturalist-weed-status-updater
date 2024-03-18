import azure.functions as func
import requests
import logging
import os

TOKEN_URL = 'https://www.inaturalist.org/oauth/token'
CREATE_OFV_URL = 'https://api.inaturalist.org/v1/observation_field_values'

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

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

@app.route(route="update")
def update(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    authorization_code = req.params.get('auth-code')
    observation_id = req.params.get('state')

    if authorization_code:
        data = {
            "observation_field_value": {
                "observation_id": observation_id,
                "observation_field_id": 42,
                "value": "n/a"
            }
        }
        api_call_headers = {'Authorization': 'Bearer ' + get_access_token(authorization_code)}
        response = requests.post(CREATE_OFV_URL, json=data, headers=api_call_headers)
        return func.HttpResponse(f"Yay! The iNaturalist observation was updated {response}!")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
