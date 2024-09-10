# Restaurant Reservation System

The Restaurant Reservation Manager is a Python - based application that empowers restaurant staff to efficiently handle customer bookings. By centralizing reservation information and automating key processes, it eliminates manual errors and ensures a smooth, organized reservation management experience.

The project can be viewed and tested [here](https://restaurant-reservation-system-13155c939e45.herokuapp.com/).

![AmIResponsive](Images/amiresponsive.png)

## Intended Users

This application is tailored for those directly involved in the day - to - day management of restaurant reservations. This includes:

- **Restaurant Owners:** Who need a clear overview of bookings and table availability.
- **Managers:** Who handle reservation inquiries, changes, and confirmations.
- **Restoraunt Staff:** Who interact with customers and need quick access to reservation details.

## Functionality

The Restaurant Reservation Manager interacts with a Google Sheet to store and retrieve reservation data. It leverages the following libraries:

- **pandas:** For working with DataFrames (tabular data structures) to represent and manipulate reservation information.
- **datetime:** For handling dates and times, ensuring proper formatting and validation.
- **gspread:** For interacting with Google Sheets API to read and write reservation data.
- **google.oauth2.service_account:** For handling authentication and authorization to access the Google Sheet.

### Core Features

1. **Add Reservation:**
   - Prompts the user to enter the following details:
     - Name (ensures unique names)
     - Date (validates for future dates only)
     - Time (validates within operating hours, 8:00 AM to 10:00 PM)
     - Number of Guests (validates for positive numbers)
   - Provides instant error messages until valid data is entered for each field, guiding the user towards successful reservation creation.
   - Appends the new reservation to the DataFrame and saves it to the Google Sheet.

   ![Add Reservation](Images/add_reservation.png)

2. **View Reservations:**
   - Fetches all reservations from the Google Sheet.
   - Sorts reservations by date and time in ascending order.
   - Presents the reservations in a clear, tabular format, including an index for easy reference.

   ![View Reservation](Images/view_reservations.png)

3. **Search Reservations:**
   - Prompts the user to enter a name to search for.
   - Filters reservations based on the entered name (case-insensitive).
   - Displays matching reservations in a tabular format.

   ![Search Reservation](Images/search_reservations.png)

4. **Delete Reservation:**
   - Displays all existing reservations.
   - Prompts the user to enter the name of the reservation to delete.
   - Deletes matching reservations from the DataFrame and saves the changes to the Google Sheet.
   - Provides feedback on the number of deleted reservations.

   ![Delete Reservation](Images/delete_reservations.png)

5. **Exit:**
   - Gracefully terminates the application, allowing the user to exit the program cleanly.

## Code Challenges and Solutions

During the development of this application, a few challenges were encountered and addressed:

- **Data Type Consistency**

  The `Date` column in the Google Sheet might be stored as text. To ensure consistent handling, the code explicitly converts it to datetime format when reading and writing data.

- **Duplicate Reservations:**

  An issue with duplicate reservations being saved was resolved by implementing a `clear()` operation on the worksheet before updating it with the latest reservation data. This ensures that the sheet is refreshed with the current state of the reservations, preventing any lingering duplicates.

## Real - Time Validation

The application incorporates real - time validation to enhance data integrity and user experience:

- **Date Validation:** Prevents the entry of past dates, ensuring that reservations are always for future events.
  - *Date formats:* If the user is asked to enter a date in the format "DD-MM-YYYY" and they type "12/31/2023" instead, that's an invalid format.
- **Time Validation:** Restricts reservation times to within the restaurant's operating hours (8:00 AM to 10:00 PM).
  - *Time formats:* Similarly, if the expected time format is "HH:MM" and the user enters "12:30 PM", that would be incorrect.
- **Name Uniqueness:** Ensures that each reservation has a unique name, avoiding confusion and potential conflicts.
- **Non - positive guest counts:** The application expects a positive number of guests for a reservation. If the user enters 0 or a negative number, that's an error.
- **Instant Feedback:** Provides immediate error messages as the user inputs data, prompting for corrections without having to complete the entire form.

## Reservation Sorting

Reservations are presented to the user in a sorted manner, making it easy to identify upcoming bookings:

- **Primary Sort:** By `Date` in ascending order, placing the nearest reservations at the top.
- **Secondary Sort:** By `Time` in ascending order, further organizing reservations within the same date.

## Potential Future Enhancements

The Restaurant Reservation Manager, while functional in its current state, holds potential for further improvements and feature additions to enhance its capabilities and user experience:

- **Maximum Capacity Management:** Implement a feature to set the maximum capacity of the restaurant. This would allow the system to automatically restrict the number of reservations that can be made at any given time, preventing overbooking and ensuring a comfortable dining experience for all guests.

- **Visual Calendar View:** Integrate a visual calendar interface to display reservations in a more intuitive and user-friendly manner. This would enable staff to quickly see available time slots and make informed decisions when accepting new bookings or managing existing ones.

- **Integration with External Systems:** Explore the possibility of integrating the reservation manager with other restaurant management systems, such as point-of-sale (POS) systems or customer relationship management (CRM) tools. This would enable seamless data sharing and streamline various operational processes.

- **Edit Reservations:** Introduce an "Edit Reservations" feature that allows users to modify existing bookings. This would provide greater flexibility for accommodating changes in guest numbers, preferred dining times, or other reservation details.

These enhancements would further elevate the Restaurant Reservation Manager's functionality, providing a more comprehensive and adaptable solution for managing restaurant reservations.
