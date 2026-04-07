from datetime import datetime
from slots import create_slots, occupy_slot, release_slot, get_remaining_time, is_slot_suitable

# --------------------------
# INITIAL SETUP
# --------------------------
slots = create_slots()   # create parking slots
RATE = 2                 # RM per hour

# --------------------------
# DISPLAY FUNCTION
# --------------------------
def display_slots():
    # Display all slots with status and vehicle info
    print("\nSlot\tType\tStatus\t     Vehicle\t     Time")
    print("--------------------------------------------------")
    for slot_id, info in slots.items():
        if info["status"] == "occupied":
            icon = "🚗"
            vehicle = f"{info['vehicle']['type']}({info['vehicle']['plate']})"
        else:
            icon = "🟢"
            vehicle = "-"
        remaining = get_remaining_time(info)
        print(f"{slot_id}\t{info['size']}\t{icon} {info['status']}\t{vehicle}\t{remaining}")

# --------------------------
# BOOKING FUNCTION
# --------------------------
def book_slot():
    try:
        slot_id = int(input("Enter slot number: "))
        hours = int(input("Enter hours to park: "))
        plate = input("Enter vehicle plate: ")
        owner = input("Enter owner name: ")
        v_type = input("Enter vehicle type (bike/car/truck): ").lower()

        if slot_id not in slots:
            print("Error: Slot does not exist.")
            return

        if slots[slot_id]["status"] == "occupied":
            print("Error: Slot already occupied.")
            return

        if not is_slot_suitable(slots[slot_id]["size"], v_type):
            print("Error: Slot not suitable for this vehicle type.")
            return

        vehicle = {
            "plate": plate,
            "owner": owner,
            "type": v_type
        }

        cost = hours * RATE
        confirm = input(f"{v_type.upper()} | {plate}\nOwner: {owner}\nHours: {hours}\nCost: RM {cost}\nConfirm? (y/n): ")
        if confirm.lower() == 'y':
            occupy_slot(slots, slot_id, hours, vehicle)
            print("Success: Slot booked successfully.")

    except ValueError:
        print("Error: Invalid input.")

# --------------------------
# EXIT FUNCTION
# --------------------------
def exit_slot():
    try:
        slot_id = int(input("Enter slot number to release: "))

        if slot_id not in slots:
            print("Error: Slot does not exist.")
            return

        if slots[slot_id]["status"] == "free":
            print("Error: Slot already free.")
            return

        slot = slots[slot_id]
        start_time = slot["start_time"]
        vehicle = slot["vehicle"]

        # calculate elapsed time
        elapsed_hours = (datetime.now().timestamp() - start_time) / 3600
        elapsed_hours = round(elapsed_hours, 2)

        total_cost = round(elapsed_hours * RATE, 2)

        print(f"\nVehicle: {vehicle['plate']}\nOwner: {vehicle['owner']}\nTime Parked: {elapsed_hours} hours\nTotal Fee: RM {total_cost}")

        release_slot(slots, slot_id)
        print("Success: Slot released.")

    except ValueError:
        print("Error: Invalid input.")

# --------------------------
# MAIN LOOP
# --------------------------
while True:
    print("\n--- Parking System ---")
    print("1. View Slots")
    print("2. Book Slot")
    print("3. Release Slot")
    print("4. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        display_slots()
    elif choice == "2":
        book_slot()
    elif choice == "3":
        exit_slot()
    elif choice == "4":
        print("Exiting system. Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")