from pprint import pprint
import os
import requests
from flight_data import FlightData

TEQUILA_LOCATIONS_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
TEQUILA_SEARCH_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"

TEQUILA_API = os.environ.get('TEQUILA_API')

headers = {
    "accept": "application/json",
    "apikey": TEQUILA_API,
}


class FlightSearch:

    def get_destination_code(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(url=TEQUILA_LOCATIONS_ENDPOINT, params=params, headers=headers)
        flight_data = response.json()["locations"][0]
        code = flight_data["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, date_from, date_to):
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "EUR",
        }

        no_flights = True
        while no_flights:
            response = requests.get(url=TEQUILA_SEARCH_ENDPOINT, params=query, headers=headers)
            try:
                data = response.json()["data"][0]
            except IndexError:
                if query["max_stopovers"] < 1:
                    query["max_stopovers"] += 1
                else:
                    print(f"No flights found for {destination_city_code}.")
                    return None
            else:
                no_flights = False

        route = {
            "Depart": [],
            "Return": []
        }
        for i in data["route"]:
            if i["return"] == 0:
                route["Depart"].append(f"{i['flyFrom']}-{i['flyTo']}")
            elif i["return"] == 1:
                route["Return"] = f"{i['flyFrom']}-{i['flyTo']}"

        if query['max_stopovers'] == 0:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["cityFrom"],
                origin_airport=data["flyFrom"],
                destination_city=data["cityTo"],
                destination_airport=data["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
                stop_overs=query['max_stopovers'],
                route=route
            )
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["cityFrom"],
                origin_airport=data["flyFrom"],
                destination_city=data["cityTo"],
                destination_airport=data["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stop_overs=query['max_stopovers'],
                via_city=data["route"][0]["cityTo"],
                route=route
            )
        print(f"{flight_data.destination_city}: {flight_data.price}€")
        return flight_data
