import azure.functions as func
import requests
import logging
import os
import json

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

@app.route(route="update", methods=(func.HttpMethod.POST,))
def update(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    authorization_code = req.params.get('auth-code')
    observation_id = req.params.get('state')
    # observation_id = base64.b64decode(req.params.get('state')).decode()
    body = req.get_body().decode()
    # logging.info('Body: ' + body)
    # try:
    #     fields = json.loads(body)
    #     logging.info("Fields: " + fields)
    #     new_observation_id = fields['observationId']
    # except:
    #     return func.HttpResponse('Unable to get observation id', 502)   
    # observation_id = body

    # try:
    #     assert observation_id == new_observation_id
    # except:
    #     return func.HttpResponse(f'observation ids dont match {observation_id} {new_observation_id}', 503)

    if authorization_code:
        data = {
            "observation_field_value": {
                "observation_id": observation_id,
                "observation_field_id": 42,
                "value": "n/a"
            }
        }
        try:
            api_call_headers = {'Authorization': 'Bearer ' + get_access_token(authorization_code)}
            response = requests.post(CREATE_OFV_URL, json=data, headers=api_call_headers)
            response.raise_for_status()
            # Process the response if the request was successful
            return func.HttpResponse(f"Yay! The iNaturalist observation was updated {response}!")
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return func.HttpResponse(e, 501)
        except Exception as e:
            logging.error(e)
            return func.HttpResponse(e, 504)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
