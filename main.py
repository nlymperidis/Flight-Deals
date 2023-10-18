import requests
from datetime import datetime, timedelta
from notification_manager import NotificationManager
from data_manager import DataManager
from flight_search import FlightSearch

ORIGIN_CITY_CODE = "ATH"

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()
sheet_data = data_manager.get_destination_data()
print(sheet_data)

# Running for the first time and don't know the iataCodes
if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

date_from = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
data_to = (datetime.now() + timedelta(days=6 * 30)).strftime("%d/%m/%Y")

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_CODE,
        destination["iataCode"],
        date_from,
        data_to
    )
    try:
        if flight.price < destination["lowestPrice"]:
            message = (f"Low price alert!\n\n "
                       f"Only {flight.price}€ "
                       f"to fly from {flight.origin_city}-{flight.origin_airport} "
                       f"to {flight.destination_city}-{flight.destination_airport}, "
                       f"from {flight.out_date} to {flight.return_date}.")
            if flight.stop_overs > 0:
                message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}"
            # ----------- SEND MESSAGE ------------ #
            notification_manager.send_sms(message)

            # ----------- SEND MAIL --------------- #
            message_mail = (f"Subject:Low price alert!\n\n Only {flight.price}€ "
                            f"to fly from {flight.origin_city}-{flight.origin_airport} "
                            f"to {flight.destination_city}-{flight.destination_airport}, "
                            f"from {flight.out_date} to {flight.return_date}.")
            notification_manager.send_emails(message_mail)
    except AttributeError:
        continue
