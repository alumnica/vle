import json
import requests
from vle_webapp.settings import XAPI_URL, XAPI_VERSION, XAPI_KEY
from webapp.statements import ComplexHandler


def send(statement):
    url = XAPI_URL
    data = json.dumps(statement, default=ComplexHandler)
    headers = {
        'X-Experience-API-Version': XAPI_VERSION,
        'Content-Type': 'application/json',
        'Authorization': XAPI_KEY
    }
    print(data)
    response = requests.post(url=url, data=data, headers=headers)
    return response