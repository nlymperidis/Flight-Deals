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

# Running for the first time and don't know the iataCodes or some are missing
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# The original date window of search is 6 months
date_from = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
data_to = (datetime.now() + timedelta(days=6 * 30)).strftime("%d/%m/%Y")

send_notif = input("Do you want to send sms/mail? Y/N: ")

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_CODE,
        destination["iataCode"],
        date_from,
        data_to
    )
    try:

        if flight.price < destination["lowestPrice"]:
            message = (f"Low price alert!\n"
                       f"Only {flight.price}€ "
                       f"to fly from {flight.origin_city}-{flight.origin_airport} "
                       f"to {flight.destination_city}-{flight.destination_airport}, "
                       f"from {flight.out_date} to {flight.return_date}.")

            if send_notif == ("Y" or "y"):
                if flight.stop_overs > 0:
                    message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}"
                # ----------- SEND MESSAGE ------------ #
                notification_manager.send_sms(message)

                # ----------- SEND MAIL --------------- #
                message_mail = f"Subject:{message}"
                notification_manager.send_emails(message_mail)
            else:
                print(f"{message}")
        else:
            print("There are no cheaper flights")

    except AttributeError:
        continue
