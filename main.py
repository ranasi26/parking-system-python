# main.py

from slots import create_slots, display_slots, release_slot
from booking import book_slot
from file_handler import save_data, load_data


def exit_parking(slots):
    try:
        slot_id = int(input("Enter slot number to release: "))
        
        if slot_id not in slots:
            print("Slot does not exist.")
            return

        if slots[slot_id]["status"] == "occupied":
            release_slot(slots, slot_id)
            print("Slot released.")
        else:
            print("Slot already free.")

    except ValueError:
        print("Invalid input.")


def main():
    slots = load_data()

    if not slots:
        slots = create_slots()
    else:
        # keys become strings after json, fix that
        slots = {int(k): v for k, v in slots.items()}

    while True:
        print("\n--- Parking System ---")
        print("1. View Slots")
        print("2. Book Slot")
        print("3. Exit Parking")
        print("4. Save & Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            display_slots(slots)

        elif choice == "2":
            book_slot(slots)

        elif choice == "3":
            exit_parking(slots)

        elif choice == "4":
            save_data(slots)
            print("Data saved. Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()