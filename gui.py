import tkinter as tk
from tkinter import messagebox
from slots import create_slots, occupy_slot, release_slot, get_free_slots
from slots import get_remaining_time

# initialize slots
slots = create_slots()

RATE = 2  # RM per hour


# ---------- FUNCTIONS ----------

def clear_placeholder(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)

def display_slots():
    output.delete("1.0", tk.END)

    output.insert(tk.END, "Slot\tStatus\tTime\n")
    output.insert(tk.END, "------------------------------\n")

    for slot_id, info in slots.items():
        if info["status"] == "occupied":
            icon = "🚗"
        else:
            icon = "🟢"

        remaining = get_remaining_time(info)

        output.insert(
            tk.END,
            f"{slot_id}\t{icon} {info['status']}\t{remaining}\n"
        )

def book_slot():
    try:
        slot_id = int(entry_slot.get())
        hours = int(entry_hours.get())

        if slot_id not in slots:
            messagebox.showerror("Error", "Slot does not exist.")
            return

        if slots[slot_id]["status"] == "occupied":
            messagebox.showerror("Error", "Slot already occupied.")
            return

        cost = hours * RATE

        confirm = messagebox.askyesno(
            "Confirm Booking",
            f"Slot {slot_id}\nHours: {hours}\nCost: RM {cost}\nConfirm?"
        )

        if confirm:
            occupy_slot(slots, slot_id, hours)
            messagebox.showinfo("Success", "Slot booked successfully.")
            display_slots()

    except ValueError:
        messagebox.showerror("Error", "Invalid input.")


def exit_slot():
    try:
        slot_id = int(entry_exit.get())

        if slot_id not in slots:
            messagebox.showerror("Error", "Slot does not exist.")
            return

        if slots[slot_id]["status"] == "free":
            messagebox.showerror("Error", "Slot already free.")
            return

        release_slot(slots, slot_id)
        messagebox.showinfo("Success", "Slot released.")
        display_slots()

    except ValueError:
        messagebox.showerror("Error", "Invalid input.")


# ---------- UI ----------

window = tk.Tk()
window.title("Parking System")
window.geometry("500x500")
window.configure(bg="#f0f8ff")  # light blue background

title = tk.Label(window, text="🚗 Parking System", font=("Arial", 18, "bold"), bg="#f0f8ff")
title.pack(pady=10)

# ---- Display button ----
btn_view = tk.Button(window, text="View Slots", bg="#4CAF50", fg="white", command=display_slots)
btn_view.pack(pady=5)

# ---- Booking section ----
tk.Label(window, text="Book Slot").pack()

entry_slot = tk.Entry(window, fg="gray")
entry_slot.insert(0, "Enter Slot Number")
entry_slot.bind("<FocusIn>", lambda e: clear_placeholder(e, entry_slot, "Enter Slot Number"))
entry_slot.pack()

entry_hours = tk.Entry(window, fg="gray")
entry_hours.insert(0, "Enter Hours")
entry_hours.bind("<FocusIn>", lambda e: clear_placeholder(e, entry_hours, "Enter Hours"))
entry_hours.pack()

btn_book = tk.Button(window, text="Book", bg="#2196F3", fg="white", command=book_slot)
btn_book.pack(pady=5)

# ---- Exit section ----
tk.Label(window, text="Exit Slot").pack()

entry_exit = tk.Entry(window, fg="gray")
entry_exit.insert(0, "Enter Slot Number")
entry_exit.bind("<FocusIn>", lambda e: clear_placeholder(e, entry_exit, "Enter Slot Number"))
entry_exit.pack()

btn_exit = tk.Button(window, text="Release Slot", bg="#f44336", fg="white", command=exit_slot)
btn_exit.pack(pady=5)

# ---- Output box ----
output = tk.Text(window, height=15, width=50, bg="#ffffff", fg="black")
output.pack(pady=10)

window.mainloop()