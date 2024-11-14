import re
import secrets
import json
import requests
from datetime import datetime
from decouple import config

ishare_map = {
    2: 50,
    4: 52,
    7: 2000,
    10: 3000,
    12: 4000,
    15: 5000,
    18: 6000,
    22: 7000,
    25: 8000,
    30: 10000,
    45: 15000,
    60: 20000,
    75: 25000,
    90: 30000,
    120: 40000,
    145: 50000,
    285: 100000,
    560: 200000
}


def ref_generator():
    now_time = datetime.now().strftime('%H%M%S')
    secret = secrets.token_hex(2)

    return f"{now_time}{secret}".upper()


def top_up_ref_generator():
    now_time = datetime.now().strftime('%H%M')
    secret = secrets.token_hex(1)

    return f"TPS-{now_time}{secret}".upper()


def send_bundle(user, receiver, bundle_amount, reference):
    try:
        url = "https://multidataghana.com/merchintegrate/geosams/ishare_api/"

        payload = {
            'type': 'pushData',
            'apikey': config('APIKEY'),
            'ref': str(reference),
            'data': str(int(bundle_amount)),
            'share': str(receiver)
        }

        response = requests.post(url, data=payload)

        try:
            response_dict = response.json()
            print("Response Dictionary:")
            print(response_dict)
            return response.status_code, response_dict
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print("Response Text:")
            print(response.text)
            return response.status_code, "bad response"
    except Exception as e:
        print(e)
        # Log the exception
        return 400, "bad response"



