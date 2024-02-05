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

    return f"TOPUP-{now_time}{secret}".upper()


def send_bundle(user, receiver, bundle_amount, reference):
    # url = "https://console.bestpaygh.com/api/flexi/v1/new_transaction/"
    #
    # headers = {
    #     "api-key": config("API_KEY"),
    #     "api-secret": config("API_SECRET"),
    #     'Content-Type': 'application/json'
    # }
    #
    # print("====================================")
    # print(user.phone)
    # print(user.first_name)
    # print(user.last_name)
    # print(user.email)
    # print(receiver)
    # print(reference)
    # print(bundle_amount)
    # print("=====================================")
    #
    # payload = json.dumps({
    #     "first_name": user.first_name,
    #     "last_name": user.last_name,
    #     "account_number": f"0{user.phone}",
    #     "receiver": receiver,
    #     "account_email": user.email,
    #     "reference": reference,
    #     "bundle_amount": bundle_amount
    # })
    #
    # response = requests.request("POST", url, headers=headers, data=payload)
    #
    # print(response.json)
    # return response

    url = "https://multidataghana.com/merchintegrate/geosams/ishare_api/"
    print(reference)
    print(bundle_amount)
    print(str(int(bundle_amount)))
    print(receiver)

    print(type(bundle_amount))
    print(type(receiver))
    payload = {'type': 'pushData',
               'apikey': config('apikey'),
               'ref': str(reference),
               'data': str(int(bundle_amount)),
               'share': str(receiver)
               }
    files = [

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    json_match = re.search(r'getBalance(.+)}', response.text)

    if json_match:
        json_part = json_match.group(1) + '}'
        print("Extracted JSON part:")
        print(json_part)

        try:
            # Parse the extracted JSON into a dictionary
            response_dict = json.loads(json_part)
            print(response_dict)

            # Now you can access the data using keys
            return response_dict
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return "bad response"
    else:
        print("No valid JSON found in the response.")
        return "bad response"


def verify_paystack_transaction(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        "Authorization": "Bearer sk_test_d8585b8c1c61a364640e9acbb3bc8046f5fb9acd"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.json())

    return response

