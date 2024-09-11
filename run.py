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
        if not data:
            self.reservations = pd.DataFrame(columns=["Name", "Date", "Time", "Number of Guests"])  # Adjust column names if needed
        else:
            self.reservations = pd.DataFrame(data[1:], columns=data[0])
        # Convert the 'Date' column to datetime format
        self.reservations['Date'] = pd.to_datetime(self.reservations['Date'], format="%d-%m-%Y", errors='coerce')
        # Convert the 'Time' column to time format
        self.reservations["Time"] = pd.to_datetime(self.reservations["Time"], format="%H:%M", errors='coerce').dt.time

    def save_reservations(self):
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
        self.worksheet.clear()
        self.worksheet.update(
            range_name='A1',
            values=[reservations_to_save.columns.values.tolist()] + reservations_to_save.values.tolist()
        )

    def add_reservation(self):
        while True:
            name = input("Enter name:\n")
            # Check if the entered name already exists in the reservations
            if name.lower() in self.reservations["Name"].str.lower().values:
                print("A reservation with this name already exists. Please enter a different name.")
            else:
                break

        while True:
            try:
                date_str = input("Enter reservation date (DD-MM-YYYY):\n")
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
                time_str = input("Enter reservation time (HH:MM):\n")
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
                number_of_guests = int(input("Enter number of guests:\n"))
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

    def search_reservations(self):
        name = input("Enter the name to search for:\n")
        # Filter reservations where the 'Name' column contains the entered name (case-insensitive)
        matching_reservations = self.reservations[
            self.reservations["Name"].str.contains(name, case=False)
        ].copy()
        # Check if the 'Date' column in the filtered reservations is already in datetime format
        if not pd.api.types.is_datetime64_any_dtype(matching_reservations['Date']):
            # If not, convert the 'Date' column to datetime, handling potential errors
            matching_reservations['Date'] = pd.to_datetime(matching_reservations['Date'], format="%d-%m-%Y", errors='coerce')
        # Check if any matching reservations were found
        if matching_reservations.empty:
            # If no matches, print a message indicating so
            print("No reservations found matching the criteria.")
        else:
            # Format the 'Date' column to a string representation in the format 'DD-MM-YYYY'
            matching_reservations['Date'] = matching_reservations['Date'].dt.strftime('%d-%m-%Y')
            # Format the 'Time' column to a string representation in the format 'HH:MM' if it's not null, otherwise leave it as an empty string
            matching_reservations['Time'] = matching_reservations['Time'].apply(lambda x: x.strftime('%H:%M') if pd.notnull(x) else '')
            # Print the matching reservations, displaying only the 'Name', 'Date', 'Time', and 'Number of Guests' columns
            print(matching_reservations[['Name', 'Date', 'Time', 'Number of Guests']].to_string(index=False))

    def delete_reservation(self):
        # Display all existing reservations
        self.view_reservations()
        # Prompt the user to enter the name of the reservation they want to delete
        name_to_delete = input("Enter the name of the reservation to delete:\n")
        # Filter the reservations DataFrame to find rows where the 'Name' column (case-insensitive) matches the entered name
        matching_reservations = self.reservations[self.reservations["Name"].str.lower() == name_to_delete.lower()]
        # Check if any matching reservations were found
        if matching_reservations.empty:
            # If no matches, print a message indicating so
            print("No reservations found matching the criteria.")
        else:
            # If matches were found:
            # Drop the matching rows from the reservations DataFrame and reset the index
            self.reservations = self.reservations.drop(matching_reservations.index).reset_index(drop=True)
            # Save the updated reservations back to the data source
            self.save_reservations()
            # Print a confirmation message indicating how many reservations were deleted and for which name
            print(f"Deleted {len(matching_reservations)} reservation(s) for {name_to_delete}")
        
def main():
    reservation_manager = ReservationManager()
    # Infinite loop that runs until the user chooses the exit option
    while True:
        print("\nRestaurant Reservation System")
        print("1. Add Reservation")
        print("2. View Reservations")
        print("3. Search Reservations")
        print("4. Delete Reservation")
        print("5. Exit")
        # Takes input from the user - their choice of option from the menu
        choice = input("Enter your choice:\n")
        if choice == "1":
            reservation_manager.add_reservation()
        elif choice == "2":
            reservation_manager.view_reservations()
        elif choice == "3":
            reservation_manager.search_reservations()
        elif choice == "4":
            reservation_manager.delete_reservation()
        # Exits the loop (and the program) if the user enters "5"
        elif choice == "5":
            break
        # Prints an error message if the user enters an invalid choice
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
if __name__ == "__main__":
    # Starts the main function of the program if the condition is met
    main()
