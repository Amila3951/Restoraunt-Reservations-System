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
        # Assign the 'reservations' worksheet to an instance variable for later use
        self.worksheet = reservations 
        # Fetch all data (including headers) from the worksheet as a list of lists
        data = self.worksheet.get_all_values()
         # Convert the 'Date' column to datetime format
        self.reservations['Date'] = pd.to_datetime(self.reservations['Date'], format="%d-%m-%Y", errors='coerce')
        # Convert the 'Time' column to time format
        self.reservations["Time"] = pd.to_datetime(self.reservations["Time"], format="%H:%M", errors='coerce').dt.time

    def save_reservations():
        # Create a copy of the reservations DataFrame to avoid modifying the original
        reservations_to_save = self.reservations.copy()
        # Check if the 'Date' column is already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(reservations_to_save['Date']):  
        # If not, convert the 'Date' column to datetime, handling potential errors
        reservations_to_save['Date'] = pd.to_datetime(reservations_to_save['Date'], errors='coerce')
        # Format the 'Date' column to a string in the desired format (DD-MM-YYYY)
    reservations_to_save['Date'] = reservations_to_save['Date'].dt.strftime('%d-%m-%Y')
    # Format the 'Time' column to a string in the desired format (HH:MM) if it's not null, otherwise set it to an empty string
    reservations_to_save['Time'] = reservations_to_save['Time'].apply(lambda x: x.strftime('%H:%M') if pd.notnull(x) else '') 
    # Replace any NaN values in the DataFrame with empty strings
    reservations_to_save.fillna('', inplace=True)  
    # Update the Google Sheet with the modified DataFrame, including column headers
    self.worksheet.update(
        # Start updating from cell A1
        range_name='A1',  
        values=[reservations_to_save.columns.values.tolist()] + reservations_to_save.values.tolist() 
    )

    def add_reservation():

    def view_reservations():

    def search_reservations():

def main():
    reservation_manager = ReservationManager()