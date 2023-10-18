# Flight Price Tracker
Flight Price Tracker is a Python application that helps you find the best flight deals from your specified origin city to various destinations. It regularly checks for flight prices and sends notifications when it finds a flight with a lower price than previously recorded.

## Getting Started

To get started with this project, follow the instructions below:

### Prerequisites

- Python 3
- Create accounts and obtain API keys for the following services:
  - Flight data (https://tequila.kiwi.com/): Obtain an API key from a flight data provider and set it in the `flight_search.py` file.
  - Your desired locations: You will need to create a sheet like this https://docs.google.com/spreadsheets/d/1zmUqfSeOZO5fmmDIaRzihbi6dUJAqOd_K7M_PN-0rRM/edit?usp=sharing .
    After that connect the sheet to https://sheety.co and set your sheety user and bearer in the `data_manager.py` file.
  - Notification services (https://www.twilio.com/): Configure the notification methods you intend to use (SMS, email) in the `notification_manager.py` file.

Usage
The application loads destination data from a spreadsheet.
If you don't know the IATA codes for destinations, it retrieves them and updates the spreadsheet.
It then checks for flight prices from your specified origin city to these destinations for a range of dates.
If a lower price is found, it sends notifications via SMS and email.

Customization
You can customize this project for your specific needs:

Modify the data_manager.py file to use your own spreadsheet format or data source.
Customize the notification methods and messages in the notification_manager.py file.
Adjust the criteria for sending price alerts in the main.py file.

Acknowledgments
This project was created as a learning exercise and is not affiliated with any flight data providers or notification services.


Make sure to update the placeholders (e.g., `yourusername`, `flight_search.py`, `notification_manager.py`, and `main.py`) with the appropriate information relevant to your project.
