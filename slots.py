# slots.py

def create_slots():
    slots = {}
    for i in range(1, 11):  # 10 slots
        slots[i] = {
            "status": "free",
            "hours": 0
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


from datetime import datetime

def occupy_slot(slots, slot_id, hours):
    slots[slot_id]["status"] = "occupied"
    slots[slot_id]["hours"] = hours
    slots[slot_id]["start_time"] = datetime.now().timestamp()


def release_slot(slots, slot_id):
    slots[slot_id]["status"] = "free"
    slots[slot_id]["hours"] = 0
    slots[slot_id]["start_time"] = None


from datetime import datetime

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