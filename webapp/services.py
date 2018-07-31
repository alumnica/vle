import json
import os

import requests

from webapp.statements import ComplexHandler


def send(statement):
    url = 'http://ec2-54-183-159-44.us-west-1.compute.amazonaws.com/data/xAPI/statements'
    data = json.dumps(statement, default=ComplexHandler)
    headers = {
        'X-Experience-API-Version': '1.0.1',
        'Content-Type': 'application/json',
        'Authorization': 'Basic YTU5YjNlOTE3NWI5ODVkYTc4Nzg4MGFjODUzZTFhZjU3Nzk3ZGM1ZDpiN2U2OTEzMjc0NzQyYjFjYzY2YjVhODVkMmZlOTVmODg5NTc0NGRm'
    }
    print(data)
    response = requests.post(url=url, data=data, headers=headers)
    return response