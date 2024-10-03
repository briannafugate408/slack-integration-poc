import os
import requests
import argparse
import creds
import csv
import time
import hmac
import hashlib
import base64
import json
import math
import urllib3


import pandas as pd

from datetime import datetime
from partner_api import generate_list_of_entrees
from server import app

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def call_partner_api_with_payload(entree_payload, api_route, hmac_secret_key):
    try:
        timestamp = math.floor(datetime.now().timestamp())
        data = f"/entree/submit-{json.dumps(entree_payload, separators=(',', ':'))}-{timestamp}"
        hashed = hmac.new(hmac_secret_key.encode(), data.encode(), hashlib.sha256)
        signature = base64.b64encode(hashed.digest()).decode()

        headers = {
            "X-Authorization": signature,
            "X-Authorization-Timestamp": str(timestamp),
        }
        response = requests.post(
            api_route, headers=headers, json=entree_payload, verify=False
        )
        response.raise_for_status()

        orderId = response.json()["entreeId"]
        print(f"Successfully submitted order with ID {orderId} to the API {api_route}")
        print("Order Payload:", entree_payload)
        print("\n\n")
        trigger_send_message(entree_payload)
    except requests.exceptions.HTTPError as err:
        print("There was an error submitting the order:", err)

def trigger_send_message(message):
    # Simulating a request to the send_message route
    print(f"Triggering send_message with message: {message}")
    with app.test_client() as client:
        response = client.post('/send-message', json={'message': message})
        return response


def main():
    # Add the CLI arguments support
    parser = argparse.ArgumentParser(
        description="Provide us the information and we'll generate entree payloads valid for testing Makeline "
        "assembly, yeet!"
    )

    parser.add_argument(
        "--hmac_secret",
        help="The Makeline you would like to route orders to. The allowed values are local. Please make sure you are on the same network as the local makeline you are trying to submit an order to.",
        metavar="",
        required=True,
    )

    customer_options = ["custom"]
    parser.add_argument(
        "--customer",
        help="The customer order data set you would like to use for testing.",
        choices=customer_options,
        required=True,
    )

    ingredient_portion_options = ["multiplier", "portion"]
    parser.add_argument(
        "--portion_type",
        help="The ingredient portion style for input.",
        choices=ingredient_portion_options,
        required=True,
    )
    args = parser.parse_args()

    hmac_secret = args.hmac_secret
    customer = args.customer
    portion_type = args.portion_type

    file_path = f"{customer}.csv"
    entree_csv_file_exists = os.path.isfile(file_path)

    if not entree_csv_file_exists:
        print(f"The file {file_path} does not exist. Please provide a valid file path.")
        exit()

    ingredient_file_path = f"ingredients_{customer}.csv"
    if not os.path.isfile(ingredient_file_path):
        print(
            f"The file {ingredient_file_path} does not exist. Please provide a valid file path."
        )
        exit()

    dtype = {"ingredient_id": str, "default_portion": int}
    default_portions = (
        pd.read_csv(ingredient_file_path, dtype=dtype)
        .to_dict(orient="records")
    )

    # Get information for makeline to route too
    makeline = creds.MAKELINE[customer]

    api_host_url = makeline["api_host_url"]

    # API URL to route orders
    api_url = api_host_url + creds.SUBMIT_ORDER_ROUTE

    with open(file_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for csv_row in reader:
            entrees_list = generate_list_of_entrees(
                csv_row, portion_type, default_portions
            )
            for entree in entrees_list:
                call_partner_api_with_payload(entree, api_url, hmac_secret)
                time.sleep(2)

if __name__ == "__main__":
    main()
