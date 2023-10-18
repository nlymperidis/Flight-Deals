import os
from twilio.rest import Client
from data_manager import DataManager
import smtplib

TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_VIRTUAL_NUMBER = os.environ.get('TWILIO_VIRTUAL_NUMBER')
TWILIO_VERIFIED_NUMBER = os.environ.get('TWILIO_VERIFIED_NUMBER')

MY_EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('PASSWORD')


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print("Text send", message.sid)
        pass

    def send_emails(self, message):
        data = DataManager()
        users_data = data.get_user_data()
        for user in users_data["users"]:
            email = user["email"]
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()  # TLS makes the connection secure
                connection.login(MY_EMAIL, PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=message.encode("utf-8")
                )
