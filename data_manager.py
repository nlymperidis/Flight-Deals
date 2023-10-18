import os
import requests

SHEETY_USER = os.environ.get('SHEETY_USER')
SHEETY_BEARER = os.environ.get('SHEETY_BEARER')

SHEETY_PRICES_ENDPOINT = f"https://api.sheety.co/{SHEETY_USER}/flightDeals/prices"
SHEETY_USERS_ENDPOINT = f"https://api.sheety.co/{SHEETY_USER}/flightDeals/users"

bearer_headers = {
    "Authorization": f"Bearer {SHEETY_BEARER}"
}


class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.users_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=bearer_headers)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=bearer_headers
            )
            print("Response text:", response.text)

    def get_user_data(self):
        response = requests.get(url=SHEETY_USERS_ENDPOINT, headers=bearer_headers)
        response.raise_for_status()
        data = response.json()
        self.users_data = data
        return self.users_data
