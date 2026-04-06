# slots.py

def create_slots():
    slots = {}

    for i in range(1, 11):
        if i <= 3:
            size = "small"   # bikes
        elif i <= 7:
            size = "medium"  # cars
        else:
            size = "large"   # trucks

        slots[i] = {
            "status": "free",
            "hours": 0,
            "size": size,
            "vehicle": None,
            "start_time": None
        }

    return slots

def display_slots(slots):
    print("\n--- Parking Slots ---")
    for slot_id, info in slots.items():
        print(f"Slot {slot_id}: {info['status']}")


def get_free_slots(slots):
    free = []
    for slot_id, info in slots.items():
        if info["status"] == "free":
            free.append(slot_id)
    return free

def is_slot_suitable(slot_size, vehicle_type):
    if vehicle_type == "bike" and slot_size == "small":
        return True
    if vehicle_type == "car" and slot_size in ["medium", "large"]:
        return True
    if vehicle_type == "truck" and slot_size == "large":
        return True
    return False


from datetime import datetime

from datetime import datetime

def occupy_slot(slots, slot_id, hours, vehicle):
    slots[slot_id]["status"] = "occupied"
    slots[slot_id]["hours"] = hours
    slots[slot_id]["vehicle"] = vehicle
    slots[slot_id]["start_time"] = datetime.now().timestamp()


def release_slot(slots, slot_id):
    slots[slot_id] = {
        "status": "free",
        "hours": 0,
        "size": slots[slot_id]["size"],
        "vehicle": None,
        "start_time": None
    }

def get_remaining_time(slot):
    if slot["status"] == "free":
        return "-"

    start = slot.get("start_time", 0)
    hours = slot["hours"]

    elapsed = (datetime.now().timestamp() - start) / 3600
    remaining = hours - elapsed

    if remaining <= 0:
        return "Time expired"
    else:
        return f"{round(remaining, 2)} hrs left"    