# slots.py

def create_slots():
    """
    Creates 10 parking slots with different sizes
    """
    slots = {}

    for i in range(1, 11):

        # assign size based on slot number
        if i <= 3:
            size = "small"   # bikes
        elif i <= 7:
            size = "medium"  # cars
        else:
            size = "large"   # trucks

        # initialize slot data
        slots[i] = {
            "status": "free",      # free or occupied
            "hours": 0,            # booked duration
            "size": size,          # slot size
            "vehicle": None,       # vehicle info
            "start_time": None     # time when parked
        }

    return slots

def display_slots(slots):
    """
    Displays all slots in CLI (old version)
    """
    print("\n--- Parking Slots ---")
    for slot_id, info in slots.items():
        print(f"Slot {slot_id}: {info['status']}")


def get_free_slots(slots):
    """
    Returns a list of all available (free) slots
    """
    free = []
    for slot_id, info in slots.items():
        if info["status"] == "free":
            free.append(slot_id)
    return free

def is_slot_suitable(slot_size, vehicle_type):
    """
    Returns a list of all available (free) slots
    """
    if vehicle_type == "bike" and slot_size == "small":
        return True
    if vehicle_type == "car" and slot_size in ["medium", "large"]:
        return True
    if vehicle_type == "truck" and slot_size == "large":
        return True
    return False

from datetime import datetime

def occupy_slot(slots, slot_id, hours, vehicle):
    """
    Marks a slot as occupied and stores vehicle details
    """
    slots[slot_id]["status"] = "occupied"
    slots[slot_id]["hours"] = hours
    slots[slot_id]["vehicle"] = vehicle

    # store current time for tracking duration
    slots[slot_id]["start_time"] = datetime.now().timestamp()


def release_slot(slots, slot_id):
    """
    Frees a slot and resets its data
    """
    slots[slot_id] = {
        "status": "free",
        "hours": 0,
        "size": slots[slot_id]["size"],
        "vehicle": None,
        "start_time": None
    }

def get_remaining_time(slot):
    """
    Calculates remaining parking time for a slot
    """
    # if slot is free → no time
    if slot["status"] == "free":
        return "-"

    start = slot.get("start_time", 0)
    hours = slot["hours"]

    # calculate time passed
    elapsed = (datetime.now().timestamp() - start) / 3600
    remaining = hours - elapsed

    # check if time finished
    if remaining <= 0:
        return "Time expired"
    else:
        return f"{round(remaining, 2)} hrs left"    