import json
import requests
from vle_webapp.settings import XAPI_URL, XAPI_VERSION, XAPI_KEY
from webapp.statements import ComplexHandler


def send(statement):
    """
    Sends Xapi statement
    :param statement: object to send
    :return: Xapi server response
    """
    try:
        url = XAPI_URL
        data = json.dumps(statement, default=ComplexHandler)
        headers = {
            'X-Experience-API-Version': XAPI_VERSION,
            'Content-Type': 'application/json',
            'Authorization': XAPI_KEY
        }
        response = requests.post(url=url, data=data, headers=headers)
    except:
        response = "Xapi connection Error"

    return response
