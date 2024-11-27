import sqlite3
from tkinter import Image, simpledialog
import customtkinter as ctk


# List of blood types (This could be dynamic if pulled from your database later)
blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# Simulating current stock for each blood type
blood_stock = {
    "A+": 1000,
    "A-": 800,
    "B+": 1200,
    "B-": 500,
    "AB+": 600,
    "AB-": 400,
    "O+": 1500,
    "O-": 900
}
def update_blood_stock(blood_type, amount, operation):
    try:
        conn = sqlite3.connect("blood_bank.db")  # Replace with your DB path
        cursor = conn.cursor()

        # Fetch the current stock
        cursor.execute("SELECT current_stock_ml FROM BLOODSTOCK WHERE blood_type = ?", (blood_type,))
        current_stock = cursor.fetchone()

        if current_stock is None:
            print(f"No record found for blood type {blood_type}.")
            return

        # Calculate the new stock
        current_stock = current_stock[0]
        if operation == "add":
            new_stock = current_stock + amount
        elif operation == "deduct":
            new_stock = current_stock - amount
            if new_stock < 0:
                print("Error: Cannot deduct more than the current stock.")
                return
        else:
            print("Invalid operation. Use 'add' or 'deduct'.")
            return

        # Update the database
        cursor.execute("UPDATE BLOODSTOCK SET current_stock_ml = ? WHERE blood_type = ?", (new_stock, blood_type))
        conn.commit()
        print(f"Updated {blood_type} stock to {new_stock} mL.")
    except Exception as e:
        print(f"Error updating blood stock: {e}")
    finally:
        conn.close()


# Function to open a small window for adding/deducting blood
def open_update_window(blood_type):
    def update_stock(action):
        """Update the stock based on the action (add or deduct)"""
        if action == "add":
            amount = simpledialog.askinteger("Add Blood", f"Enter amount to add for {blood_type}:")
            if amount:
                blood_stock[blood_type] += amount
        elif action == "deduct":
            amount = simpledialog.askinteger("Deduct Blood", f"Enter amount to deduct for {blood_type}:")
            if amount and blood_stock[blood_type] >= amount:
                blood_stock[blood_type] -= amount
            else:
                print("Insufficient stock or invalid amount.")
        print(f"Updated {blood_type}: {blood_stock[blood_type]} mL")

    # Create a new window for adding or deducting stock
    window = ctk.CTkToplevel()
    window.title(f"Manage Stock for {blood_type}")
    window.geometry("300x200")

    # Create Add and Deduct buttons
    add_button = ctk.CTkButton(window, text="Add Blood", command=lambda: update_stock("add"))
    add_button.place(relx=0.5, rely=0.4, anchor="center")

    deduct_button = ctk.CTkButton(window, text="Deduct Blood", command=lambda: update_stock("deduct"))
    deduct_button.place(relx=0.5, rely=0.6, anchor="center")

    # Label to show the current stock
    stock_label = ctk.CTkLabel(window, text=f"Current stock: {blood_stock[blood_type]} mL")
    stock_label.place(relx=0.5, rely=0.2, anchor="center")



# Blood Stock Page UI
def bloodstock_ui():
    # Create the window
    root = ctk.CTk()
    root.title("Blood Stock Management")
    root.geometry("800x400")

    # Create a 4x2 grid of blood types
    for i, blood_type in enumerate(blood_types):
        # Calculate row and column position for the 4x2 grid
        row = i // 4
        col = i % 4

        # Create a button with an image (if available) for each blood type
        button = ctk.CTkButton(root, text=blood_type, width=180, height=100,
                               command=lambda b=blood_type: open_update_window(b))

        # Place button in the grid
        button.grid(row=row, column=col, padx=10, pady=10)

    current_total_label = ctk.CTkLabel(root, text="Current Total: ", width=400, height=50, anchor="center", fg_color="#702963")
    current_total_label.grid(row=4, column=0, columnspan=2, pady=10)

    # Row 5, Column 0 and 1 will be the "All-Time Total" label (spanning 2 columns)
    all_time_total_label = ctk.CTkLabel(root, text="All-Time Total: ", width=400, height=50, anchor="center", fg_color="#702963")
    all_time_total_label.grid(row=4, column=2, columnspan=2, pady=10)

    root.grid_rowconfigure(0, weight=1)  # Top empty space
    root.grid_rowconfigure(1, weight=0)  # Row for the first row of buttons
    root.grid_rowconfigure(2, weight=0)  # Row for the second row of buttons
    root.grid_rowconfigure(3, weight=0)  # Row for spacing
    root.grid_rowconfigure(4, weight=0)  # Row for Current Total label
    root.grid_rowconfigure(5, weight=0)  # Row for All-Time Total label
    root.grid_rowconfigure(6, weight=1)  # Bottom empty space

    root.grid_columnconfigure(0, weight=1)  # Left empty space
    root.grid_columnconfigure(1, weight=0)  # Buttons and labels
    root.grid_columnconfigure(2, weight=0)  # Buttons and labels
    root.grid_columnconfigure(3, weight=0)  # Buttons and labels
    root.grid_columnconfigure(4, weight=1)

    # Start the UI loop
    root.mainloop()

# Run the Blood Stock UI
bloodstock_ui()
# open_update_window()


def donations_ui():
    pass


def requests_ui():
    pass


def display_allhistory():
    pass


def view_userlist():
    pass