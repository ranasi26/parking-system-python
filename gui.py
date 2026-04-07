import tkinter as tk
from tkinter import messagebox
from slots import (
    create_slots,
    occupy_slot,
    release_slot,
    get_remaining_time,
    is_slot_suitable
)

# =========================================
# INITIAL SETUP
# =========================================

slots = create_slots()   # create parking slots
RATE = 2                 # RM per hour


# =========================================
# HELPER FUNCTIONS
# =========================================

def clear_placeholder(event, entry, placeholder):
    """Clears placeholder text when user clicks input field"""
    if entry.get() == placeholder:
        entry.delete(0, tk.END)


# =========================================
# DISPLAY FUNCTION
# =========================================

def display_slots():
    """Display all parking slots with status and vehicle info"""
    output.delete("1.0", tk.END)

    output.insert(tk.END, "Slot\tType\tStatus\t     Vehicle\t     Time\n")
    output.insert(tk.END, "--------------------------------------------------\n")

    for slot_id, info in slots.items():
        # Determine icon and vehicle display
        if info["status"] == "occupied":
            icon = "🚗"
            vehicle = f"  {info['vehicle']['type']}({info['vehicle']['plate']})"
        else:
            icon = "🟢"
            vehicle = "-"

        # Get remaining time
        remaining = get_remaining_time(info)

        # Print formatted row
        output.insert(
            tk.END,
            f"{slot_id}\t{info['size']}\t{icon} {info['status']}\t{vehicle}\t{remaining}\n"
        )

# =========================================
# BOOKING FUNCTION
# =========================================

def book_slot():
    """Handles booking logic"""
    try:
        # Get user input
        slot_id = int(entry_slot.get())
        hours = int(entry_hours.get())
        plate = entry_plate.get()
        owner = entry_owner.get()
        v_type = entry_type.get().lower()

        # Validation checks
        if slot_id not in slots:
            messagebox.showerror("Error", "Slot does not exist.")
            return

        if slots[slot_id]["status"] == "occupied":
            messagebox.showerror("Error", "Slot already occupied.")
            return

        # Check vehicle compatibility
        if not is_slot_suitable(slots[slot_id]["size"], v_type):
            messagebox.showerror("Error", "Slot not suitable for this vehicle type.")
            return

        # Store vehicle data
        vehicle = {
            "plate": plate,
            "owner": owner,
            "type": v_type
        }

        # Calculate cost
        cost = hours * RATE

        # Confirmation popup
        confirm = messagebox.askyesno(
            "Confirm Booking",
            f"{v_type.upper()} | {plate}\nOwner: {owner}\nHours: {hours}\nCost: RM {cost}\nConfirm?"
        )

        # Final booking
        if confirm:
            occupy_slot(slots, slot_id, hours, vehicle)
            messagebox.showinfo("Success", "Slot booked successfully.")
            display_slots()

    except ValueError:
        messagebox.showerror("Error", "Invalid input.")


# =========================================
# EXIT FUNCTION
# =========================================

from datetime import datetime

def exit_slot():
    try:
        slot_id = int(entry_exit.get())

        if slot_id not in slots:
            messagebox.showerror("Error", "Slot does not exist.")
            return

        if slots[slot_id]["status"] == "free":
            messagebox.showerror("Error", "Slot already free.")
            return

        # GET SLOT DATA BEFORE RELEASING
        slot = slots[slot_id]

        start_time = slot["start_time"]
        vehicle = slot["vehicle"]

        # calculate actual time used
        elapsed_hours = (datetime.now().timestamp() - start_time) / 3600
        elapsed_hours = round(elapsed_hours, 2)

        # calculate fee
        total_cost = elapsed_hours * RATE
        total_cost = round(total_cost, 2)

        # show result
        messagebox.showinfo(
            "Payment Info",
            f"Vehicle: {vehicle['plate']}\n"
            f"Owner: {vehicle['owner']}\n"
            f"Time Parked: {elapsed_hours} hours\n"
            f"Total Fee: RM {total_cost}"
        )

        # release slot AFTER calculation
        release_slot(slots, slot_id)

        messagebox.showinfo("Success", "Slot released.")
        display_slots()

    except ValueError:
        messagebox.showerror("Error", "Invalid input.")


# =========================================
# GUI LAYOUT
# =========================================

window = tk.Tk()
window.title("Parking System")
window.geometry("550x600")
window.configure(bg="#f0f8ff")


# ---------- TITLE ----------
title = tk.Label(
    window,
    text="🚗 Parking System 🚗",
    font=("Arial", 18, "bold"),
    bg="#f0f8ff"
)
title.pack(pady=10)


# ---------- VIEW BUTTON ----------
btn_view = tk.Button(
    window,
    text="View Slots",
    bg="#4CAF50",
    fg="white",
    command=display_slots
)
btn_view.pack(pady=5)


# =========================================
# BOOKING SECTION
# =========================================

tk.Label(window, text="--- Book Slot ---", bg="#f0f8ff").pack(pady=5)

entry_slot = tk.Entry(window, fg="gray", width=30)
entry_slot.insert(0, "Enter Slot Number")
entry_slot.bind("<FocusIn>", lambda e: clear_placeholder(e, entry_slot, "Enter Slot Number"))
entry_slot.pack(pady=2)

entry_hours = tk.Entry(window, fg="gray", width=30)
entry_hours.insert(0, "Enter Hours")
entry_hours.bind("<FocusIn>", lambda e: clear_placeholder(e, entry_hours, "Enter Hours"))
entry_hours.pack(pady=2)

entry_plate = tk.Entry(window, fg="gray", width=30)
entry_plate.insert(0, "Plate Number")
entry_plate.bind("<FocusIn>", lambda e: clear_placeholder(e, entry_plate, "Plate Number"))
entry_plate.pack(pady=2)

entry_owner = tk.Entry(window, fg="gray", width=30)
entry_owner.insert(0, "Owner Name")
entry_owner.bind("<FocusIn>", lambda e: clear_placeholder(e, entry_owner, "Owner Name"))
entry_owner.pack(pady=2)

entry_type = tk.Entry(window, fg="gray", width=30)
entry_type.insert(0, "Vehicle Type (bike/car/truck)")
entry_type.bind("<FocusIn>", lambda e: clear_placeholder(e, entry_type, "Vehicle Type (bike/car/truck)"))
entry_type.pack(pady=2)

btn_book = tk.Button(
    window,
    text="Book Slot",
    bg="#2196F3",
    fg="white",
    command=book_slot
)
btn_book.pack(pady=5)


# =========================================
# EXIT SECTION
# =========================================

tk.Label(window, text="--- Exit Parking ---", bg="#f0f8ff").pack(pady=5)

entry_exit = tk.Entry(window, fg="gray")
entry_exit.insert(0, "Enter Slot Number")
entry_exit.bind("<FocusIn>", lambda e: clear_placeholder(e, entry_exit, "Enter Slot Number"))
entry_exit.pack(pady=2)

btn_exit = tk.Button(
    window,
    text="Release Slot",
    bg="#f44336",
    fg="white",
    command=exit_slot
)
btn_exit.pack(pady=5)


# =========================================
# OUTPUT DISPLAY
# =========================================

output = tk.Text(window, height=15, width=60, bg="white", fg="black")
output.pack(pady=10)


# =========================================
# RUN APP
# =========================================

window.mainloop()