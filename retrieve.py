import json

import dotenv
import requests
import os
import sys


def retrieve_and_save(obj_type: str, endpoint: str = None, save: bool = True) -> list[dict]:
    dotenv.load_dotenv()

    BASE_URI: str = "https://mycrm.zendesk.com/api/v2"
    endpoint = endpoint or obj_type

    usr_email: str = os.getenv("ZENDESK_EMAIL")
    usr_token: str = os.getenv("ZENDESK_TOKEN")

    usr = f"{usr_email}/token"

    url: str = f"{BASE_URI}/{endpoint}.json?page=1"

    data = []

    while url is not None:
        req = requests.get(url, auth=(usr, usr_token))

        # print(f"Retrieved data from url: {url}")

        try:
            data += req.json().get(obj_type)
        except TypeError as e:
            print(e)
            print(req.json())

        url = req.json().get("next_page")

    if save:
        with open(f"data/{endpoint}.json", "w") as f:
            f.write(json.dumps(data))

    return data


if __name__ == '__main__':
    object_type = sys.argv[1] if len(sys.argv) > 1 else input("Object type: ")
    retrieve_and_save(object_type)
