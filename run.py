# Import the pandas library for working with DataFrames (tabular data structures)
import pandas as pd
 # Import the datetime library for handling dates and times
import datetime
 # Import the gspread library for interacting with Google Sheets API
import gspread
# Import the Credentials class
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

    def add_reservation(self):
        while True:
            name = input("Enter name: ")
            # Check if the entered name already exists in the reservations
            if name.lower() in self.reservations["Name"].str.lower().values:
                print("A reservation with this name already exists. Please enter a different name.")
            else:
                break

        while True:
            try:
                date_str = input("Enter reservation date (DD-MM-YYYY): ")
                date = datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
                # Check if the entered date is in the past
                if date < datetime.date.today():
                    raise ValueError("Reservation date cannot be in the past.")
                break
            except ValueError as e:
                # Print an error message if the date is invalid or in the past
                print(f"Invalid date format or past date: {e}")

        while True:
                try:
                    time_str = input("Enter reservation time (HH:MM): ")
                    time = datetime.datetime.strptime(time_str, "%H:%M").time()
                    # Check if the entered time is within operating hours (8:00 AM to 10:00 PM)
                    if time < datetime.time(8, 0) or time > datetime.time(22, 0):
                        raise ValueError("Our hours of operation are from 8:00 AM to 10:00 PM. Please select a reservation time within this range.")
                    break
                except ValueError as e:
                    # Print an error message if the time is invalid or outside operating hours
                    print(f"Invalid time format or outside operating hours: {e}")

        while True:
            try:
                number_of_guests = int(input("Enter number of guests: "))
                 # Check if the entered number of guests is positive
                if number_of_guests <= 0:
                    raise ValueError("Number of guests must be positive.")
                break
            except ValueError as e:
                # Print an error message if the number of guests is invalid or not positive
                print(f"Invalid number: {e}")

        columns = self.reservations.columns.tolist()
        new_reservation = pd.DataFrame(
            {
                "Name": [name],
                "Date": [date],
                "Time": [time],
                "Number of Guests": [number_of_guests],
            },
            # Ensure the new DataFrame has the same column names as the existing one
            columns=columns
        )
         # Convert the 'Date' column in the new reservation DataFrame to datetime format
        new_reservation['Date'] = pd.to_datetime(new_reservation['Date']) 
        # Append the new reservation to the existing reservations DataFrame
        self.reservations = pd.concat([self.reservations, new_reservation], ignore_index=True)
        self.save_reservations()
        print("Reservation added successfully!")

    def view_reservations(self):
        if self.reservations.empty:
            print("No reservations found.")
        else:
            if not pd.api.types.is_datetime64_any_dtype(self.reservations['Date']):
                # Check if the 'Date' column is already in datetime format, if not, convert it
                self.reservations['Date'] = pd.to_datetime(self.reservations['Date'], format="%d-%m-%Y", errors='coerce')
            # Sort the reservations DataFrame by 'Date' and 'Time' in ascending order
            sorted_reservations = self.reservations.sort_values(["Date", "Time"], ascending=[True, True])
             # Insert a new column 'Index' at the beginning, starting from 1 and incrementing for each row
            sorted_reservations.insert(0, 'Index', range(1, len(sorted_reservations) + 1))
             # Format the 'Date' column to a string representation in the format 'DD-MM-YYYY'
            sorted_reservations['Date'] = sorted_reservations['Date'].dt.strftime('%d-%m-%Y')
             # Format the 'Time' column to a string representation in the format 'HH:MM' if it's not null, otherwise leave it as an empty string
            sorted_reservations['Time'] = sorted_reservations['Time'].apply(lambda x: x.strftime('%H:%M') if pd.notnull(x) else '')
            # Print the sorted reservations, displaying only the 'Index', 'Name', 'Date', 'Time', and 'Number of Guests' columns
            print(sorted_reservations[["Index", "Name", "Date", "Time", "Number of Guests"]].to_string(index=False))

    def search_reservations():

def main():
    reservation_manager = ReservationManager()