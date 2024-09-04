import pandas as pd
import datetime
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("ReservationManager")
reservations = SHEET.worksheet("reservations")

class ReservationManager:
    def __init__(self):
        self.worksheet = reservations
        data = self.worksheet.get_all_values()
        self.reservations['Date'] = pd.to_datetime(self.reservations['Date'], format="%d-%m-%Y", errors='coerce')
        self.reservations["Time"] = pd.to_datetime(self.reservations["Time"], format="%H:%M", errors='coerce').dt.time

    def save_reservations():

    def add_reservation():

    def view_reservations():

    def search_reservations():

def main():
    reservation_manager = ReservationManager()