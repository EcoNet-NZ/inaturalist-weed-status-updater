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

def update_observation_fields(json, access_token):
    api_call_headers = {'Authorization': 'Bearer ' + access_token}

    try:
        observation_id = json['observationId']
    except:
        return func.HttpResponse("No observation id in json body", 400)

    for key, value in json.items():
        if key != 'observationId':
            logging.info(f'Updating {key} to {value}')
            data = {
                "observation_field_value": {
                    "observation_id": observation_id,
                    "observation_field_id": key,
                    "value": value
                }
            }
        try:    
            response = requests.post(CREATE_OFV_URL, json=data, headers=api_call_headers)
            response.raise_for_status()
        # except requests.exceptions.RequestException as e:
        #     logging.error(e)
        #     return func.HttpResponse(e, 500)
        except Exception as e:
            logging.error(e)
            return func.HttpResponse(e, 500)
        
    return func.HttpResponse(f"Yay! The iNaturalist observation was updated {response}!")


@app.route(route="update", methods=(func.HttpMethod.POST,))
def update(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        authorization_code = req.params.get('auth-code')
    except:
        return func.HttpResponse("Unable to read 'auth-code' parameter", 400)
    
    if not authorization_code:
        return func.HttpResponse("Missing parameter 'auth-code'", 400)

    try:
        access_token = get_access_token(authorization_code)
    except:
        return func.HttpResponse("Unable to get authorization code", 401)
        
    try:
        json = req.get_json()
        logging.info(f'Request body: {json}')
    except:
        return func.HttpResponse("Unable to parse json body", 400)
    
    return update_observation_fields(json, access_token)