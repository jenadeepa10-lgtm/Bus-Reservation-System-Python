import json
import os
DATA_FILE = "bookings.json"
buses = {
    "B101": {
        "route": "Pune -> Mumbai",
        "departure": "08:00 AM",
        "arrival": "12:00 PM",
        "total_seats": 10,
        "fare": 450
    },

    "B102": {
        "route": "Pune -> Nashik",
        "departure": "09:30 AM",
        "arrival": "01:00 PM",
        "total_seats": 12,
        "fare": 350
    }
}

bookings = {}

# CLASS 1 : PASSENGER
# ==========================================================

class Passenger:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_details(self):
        print(f"Passenger : {self.name}")
        print(f"Age       : {self.age}")

# ==========================================================
# CLASS 2 : BOOKING
# ==========================================================

class Booking:

    def __init__(
        self,
        booking_id,
        passenger,
        journey_id,
        seat_number,
        fare,
        status="CONFIRMED"
    ):

        self.booking_id = booking_id
        self.passenger = passenger
        self.journey_id = journey_id
        self.seat_number = seat_number
        self.fare = fare
        self.status = status

    def display_booking(self):

        bus = buses[self.journey_id]

        print("\n" + "=" * 45)
        print("             BOOKING DETAILS")
        print("=" * 45)

        print(f"Booking ID : {self.booking_id}")
        print(f"Passenger  : {self.passenger.name}")
        print(f"Age        : {self.passenger.age}")
        print(f"Journey    : {self.journey_id}")
        print(f"Route      : {bus['route']}")
        print(f"Departure  : {bus['departure']}")
        print(f"Arrival    : {bus['arrival']}")
        print(f"Seat       : {self.seat_number:02d}")
        print(f"Fare       : ₹{self.fare}")
        print(f"Status     : {self.status}")

        print("=" * 45)

# ==========================================================
# VIEW BUSES
# ==========================================================

def view_buses():

    print("\n" + "-" * 75)
    print(
        f"{'ID':<8}"
        f"{'ROUTE':<22}"
        f"{'TIME':<15}"
        f"{'FARE':<10}"
        f"{'SEATS':<10}"
    )

    print("-" * 75)

    for bus_id, bus in buses.items():

        available = get_available_seats(bus_id)

        time = bus["departure"]

        print(
            f"{bus_id:<8}"
            f"{bus['route']:<22}"
            f"{time:<15}"
            f"₹{bus['fare']:<9}"
            f"{len(available):<10}"
        )

    print("-" * 75)


# ==========================================================
# GET AVAILABLE SEATS
# ==========================================================

def get_available_seats(journey_id):

    total_seats = buses[journey_id]["total_seats"]

    booked_seats = {
        booking.seat_number
        for booking in bookings.values()
        if booking.journey_id == journey_id
        and booking.status == "CONFIRMED"
    }

    available_seats = [
        seat
        for seat in range(1, total_seats + 1)
        if seat not in booked_seats
    ]

    return available_seats


# ==========================================================
# VIEW AVAILABLE SEATS
# ==========================================================

def view_seats():

    view_buses()

    journey_id = input(
        "\nEnter Journey ID: "
    ).strip().upper()

    if journey_id not in buses:

        print("Invalid Journey ID.")

        return

    available_seats = get_available_seats(journey_id)

    total_seats = buses[journey_id]["total_seats"]

    booked_seats = set(range(1, total_seats + 1)) - set(
        available_seats
    )

    print("\n" + "=" * 35)
    print(f"              BUS {journey_id}")
    print("=" * 35)

    # Display seats in rows
    for seat in range(1, total_seats + 1, 2):

        seat1 = f"[{seat:02d}]"

        if seat in booked_seats:
            seat1 += " X"
        else:
            seat1 += " O"

        if seat + 1 <= total_seats:

            seat2 = f"[{seat + 1:02d}]"

            if seat + 1 in booked_seats:
                seat2 += " X"
            else:
                seat2 += " O"

            print(f"{seat1:<10}{seat2}")

        else:

            print(seat1)

    print("\nO = Available")
    print("X = Booked")

    print("\nAvailable:")
    print(
        " ".join(
            f"{seat:02d}"
            for seat in available_seats
        )
    )

    print("\nBooked:")

    if booked_seats:
        print(
            " ".join(
                f"{seat:02d}"
                for seat in sorted(booked_seats)
            )
        )
    else:
        print("None")


# ==========================================================
# CALCULATE FARE
# ==========================================================

def calculate_fare(base_fare, age):

    # Age below 12 -> 50% discount
    if age < 12:

        fare = base_fare * 0.50

    # Age 12-59 -> Full fare
    elif age <= 59:

        fare = base_fare

    # Age 60+ -> 30% discount
    else:

        fare = base_fare * 0.70

    return round(fare, 2)


# ==========================================================
# GENERATE UNIQUE BOOKING ID
# ==========================================================

def generate_booking_id():

    if not bookings:

        return "ST1001"

    numbers = []

    for booking_id in bookings:

        try:

            number = int(
                booking_id.replace("ST", "")
            )

            numbers.append(number)

        except ValueError:

            pass

    if numbers:

        next_number = max(numbers) + 1

    else:

        next_number = 1001

    return f"ST{next_number}"


# ==========================================================
# BOOK TICKET
# ==========================================================

def book_ticket():

    view_buses()

    # ------------------------------------------------------
    # JOURNEY ID
    # ------------------------------------------------------

    journey_id = input(
        "\nEnter Journey ID: "
    ).strip().upper()

    if journey_id not in buses:

        print("Invalid Journey ID.")

        return

    # ------------------------------------------------------
    # AVAILABLE SEATS
    # ------------------------------------------------------

    available_seats = get_available_seats(journey_id)

    if not available_seats:

        print("\nSorry! No seats are available.")

        return

    print("\nAvailable Seats:")

    print(
        " ".join(
            f"{seat:02d}"
            for seat in available_seats
        )
    )

    # ------------------------------------------------------
    # PASSENGER NAME
    # ------------------------------------------------------

    while True:

        name = input(
            "\nEnter passenger name: "
        ).strip()

        if name:

            name = name.title()

            break

        print("Passenger name cannot be empty.")

    # ------------------------------------------------------
    # AGE
    # ------------------------------------------------------

    while True:

        try:

            age = int(
                input("Enter age: ")
            )

            if age <= 0:

                print("Age must be greater than 0.")

            else:

                break

        except ValueError:

            print("Invalid input.")
            print("Age must be a number.")
            print("Please try again.")

    # ------------------------------------------------------
    # SEAT NUMBER
    # ------------------------------------------------------

    while True:

        try:

            seat_number = int(
                input("Select seat: ")
            )

            if seat_number not in available_seats:

                print(
                    "Invalid or already booked seat."
                )

            else:

                break

        except ValueError:

            print(
                "Please enter a valid seat number."
            )

    # ------------------------------------------------------
    # CREATE PASSENGER OBJECT
    # ------------------------------------------------------

    passenger = Passenger(
        name,
        age
    )

    # ------------------------------------------------------
    # CALCULATE FARE
    # ------------------------------------------------------

    base_fare = buses[journey_id]["fare"]

    fare = calculate_fare(
        base_fare,
        age
    )

    # ------------------------------------------------------
    # GENERATE BOOKING ID
    # ------------------------------------------------------

    booking_id = generate_booking_id()

    # ------------------------------------------------------
    # CREATE BOOKING OBJECT
    # ------------------------------------------------------

    booking = Booking(
        booking_id,
        passenger,
        journey_id,
        seat_number,
        fare
    )

    # ------------------------------------------------------
    # SAVE BOOKING
    # ------------------------------------------------------

    bookings[booking_id] = booking

    save_data()

    # ------------------------------------------------------
    # CONFIRMATION
    # ------------------------------------------------------

    print("\nProcessing booking...")

    print("\n" + "=" * 45)
    print("             BOOKING CONFIRMED")
    print("=" * 45)

    print(f"Booking ID : {booking_id}")
    print(f"Passenger  : {name}")
    print(f"Journey    : {journey_id}")
    print(f"Route      : {buses[journey_id]['route']}")
    print(f"Seat       : {seat_number:02d}")
    print(f"Fare       : ₹{fare}")
    print("Status     : CONFIRMED")

    print("=" * 45)


# ==========================================================
# CANCEL TICKET
# ==========================================================

def cancel_ticket():

    booking_id = input(
        "\nEnter Booking ID: "
    ).strip().upper()

    if booking_id not in bookings:

        print("Booking not found.")

        return

    booking = bookings[booking_id]

    if booking.status == "CANCELLED":

        print("This booking is already cancelled.")

        return

    print("\nBooking found.")

    print(
        f"Passenger: {booking.passenger.name}"
    )

    print(
        f"Seat: {booking.seat_number:02d}"
    )

    while True:

        choice = input(
            "\nCancel booking? (yes/no): "
        ).strip().lower()

        if choice in ["yes", "no"]:
            break

        print("Please enter yes or no.")

    if choice == "yes":

        booking.status = "CANCELLED"

        save_data()

        print("\nBooking cancelled successfully.")

        print(
            f"Seat {booking.seat_number:02d} "
            "is now available."
        )

    else:

        print("\nBooking cancellation aborted.")


# ==========================================================
# VIEW BOOKING
# ==========================================================

def view_booking():

    booking_id = input(
        "\nEnter Booking ID: "
    ).strip().upper()

    if booking_id not in bookings:

        print("Booking not found.")

        return

    booking = bookings[booking_id]

    booking.display_booking()


# ==========================================================
# SEARCH PASSENGER / BOOKING
# ==========================================================

def search_booking():

    search_value = input(
        "\nEnter passenger name or booking ID: "
    ).strip().lower()

    if not search_value:

        print("Search value cannot be empty.")

        return

    found = False

    print("\nSearch Results")
    print("-" * 45)

    for booking in bookings.values():

        passenger_name = (
            booking.passenger.name.lower()
        )

        booking_id = (
            booking.booking_id.lower()
        )

        # Partial passenger name search
        if (
            search_value in passenger_name
            or search_value == booking_id
        ):

            found = True

            print(
                f"Booking ID : {booking.booking_id}"
            )

            print(
                f"Passenger  : "
                f"{booking.passenger.name}"
            )

            print(
                f"Journey    : "
                f"{booking.journey_id}"
            )

            print(
                f"Route      : "
                f"{buses[booking.journey_id]['route']}"
            )

            print(
                f"Seat       : "
                f"{booking.seat_number:02d}"
            )

            print(
                f"Fare       : ₹{booking.fare}"
            )

            print(
                f"Status     : {booking.status}"
            )

            print("-" * 45)

    if not found:

        print("No matching booking found.")


# ==========================================================
# SAVE DATA TO FILE
# ==========================================================

def save_data():

    data = {}

    for booking_id, booking in bookings.items():

        data[booking_id] = {

            "booking_id": booking.booking_id,

            "passenger_name":
                booking.passenger.name,

            "age":
                booking.passenger.age,

            "journey_id":
                booking.journey_id,

            "seat_number":
                booking.seat_number,

            "fare":
                booking.fare,

            "status":
                booking.status
        }

    try:

        with open(DATA_FILE, "w") as file:

            json.dump(
                data,
                file,
                indent=4
            )

    except IOError:

        print(
            "Error: Could not save booking data."
        )


# ==========================================================
# LOAD DATA FROM FILE
# ==========================================================

def load_data():

    global bookings

    if not os.path.exists(DATA_FILE):

        bookings = {}

        return

    try:

        with open(DATA_FILE, "r") as file:

            data = json.load(file)

        bookings = {}

        for booking_id, details in data.items():

            passenger = Passenger(
                details["passenger_name"],
                details["age"]
            )

            booking = Booking(
                details["booking_id"],
                passenger,
                details["journey_id"],
                details["seat_number"],
                details["fare"],
                details["status"]
            )

            bookings[booking_id] = booking

    except (json.JSONDecodeError, KeyError):

        print(
            "Warning: Booking file contains "
            "invalid data."
        )

        bookings = {}

    except IOError:

        print(
            "Error: Could not load booking data."
        )

        bookings = {}


# ==========================================================
# MAIN PROGRAM
# ==========================================================

def main():

    # Load previous bookings
    load_data()

    while True:

        display_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        # -----------------------------------------------
        # VIEW BUSES
        # -----------------------------------------------

        if choice == "1":

            view_buses()

        # -----------------------------------------------
        # VIEW SEATS
        # -----------------------------------------------

        elif choice == "2":

            view_seats()

        # -----------------------------------------------
        # BOOK TICKET
        # -----------------------------------------------

        elif choice == "3":

            book_ticket()

        # -----------------------------------------------
        # CANCEL TICKET
        # -----------------------------------------------

        elif choice == "4":

            cancel_ticket()

        # -----------------------------------------------
        # VIEW BOOKING
        # -----------------------------------------------

        elif choice == "5":

            view_booking()

        # -----------------------------------------------
        # SEARCH
        # -----------------------------------------------

        elif choice == "6":

            search_booking()

        # -----------------------------------------------
        # EXIT
        # -----------------------------------------------

        elif choice == "7":

            print("\nThank you for using SwiftTravel.")
            print("Have a safe journey!")

            break

        # -----------------------------------------------
        # INVALID MENU CHOICE
        # -----------------------------------------------

        else:

            print(
                "\nInvalid choice."
            )

            print(
                "Please enter a number from 1 to 7."
            )


# ==========================================================
# PROGRAM START
# ==========================================================

if __name__ == "__main__":

    main()