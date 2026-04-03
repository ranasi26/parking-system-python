# booking.py

RATE_PER_HOUR = 2  # RM 2/hour


def calculate_cost(hours):
    return hours * RATE_PER_HOUR


def book_slot(slots):
    from slots import get_free_slots, occupy_slot

    free_slots = get_free_slots(slots)

    if not free_slots:
        print("No available slots.")
        return

    print("Available slots:", free_slots)

    try:
        slot_id = int(input("Choose a slot: "))
        if slot_id not in free_slots:
            print("Invalid or occupied slot.")
            return

        hours = int(input("Enter number of hours: "))
        cost = calculate_cost(hours)

        print(f"Total cost: RM {cost}")

        confirm = input("Confirm booking? (y/n): ").lower()
        if confirm == "y":
            occupy_slot(slots, slot_id, hours)
            print("Slot booked successfully.")
        else:
            print("Booking cancelled.")

    except ValueError:
        print("Invalid input.")