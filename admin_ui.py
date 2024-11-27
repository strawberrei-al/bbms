import sqlite3
from tkinter import Image, simpledialog
import customtkinter as ctk


# List of blood types (This could be dynamic if pulled from your database later)
# blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# Simulating current stock for each blood type
blood_stock = {"A+","A-","B+","B-","AB+","AB-","O+","O-"}


def update_blood_stock(blood_type, amount, operation, root=None):
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
            print("Invalid operation. Use add or deduct.")
            return

        # Update the database
        cursor.execute("UPDATE BLOODSTOCK SET current_stock_ml = ? WHERE blood_type = ?", (new_stock, blood_type))
        conn.commit()
        print(f"Updated {blood_type} stock to {new_stock} mL.")

        if root:
            refresh_bloodstockUI(root)

    except Exception as e:
        print(f"Error updating blood stock: {e}")
    finally:
        conn.close()


def refresh_bloodstockUI(root):
    blood_stock = fetch_blood_stock()  # Fetch the latest stock data from the database

    # Clear the previous buttons in the UI
    for widget in root.winfo_children():
        if isinstance(widget, ctk.CTkButton):
            widget.destroy()

    # Create a 4x2 grid of blood types with updated stock
    for i, (blood_type, stock) in enumerate(blood_stock.items()):
        # Calculate row and column position for the 4x2 grid
        row = i // 4
        col = i % 4

        # Create a button with updated stock values for each blood type
        button = ctk.CTkButton(root, text=f"{blood_type}\n{stock} mL", width=180, height=100,
                               command=lambda b=blood_type: open_update_window(b,root))

        # Place button in the grid
        button.grid(row=row, column=col, padx=10, pady=10)

    # Optionally update any other UI elements (like total stock) if necessary.
    # For example, you could recalculate and display the current total stock.


# Function to open a small window for adding/deducting blood
def open_update_window(blood_type, root):
    def update_stock(action):
        conn = sqlite3.connect("blood_bank.db")
        cursor = conn.cursor()

        """Update the stock based on the action (add or deduct)"""
        if action == "add":
            amount = simpledialog.askinteger("Add Blood", f"Enter amount to add for {blood_type}:")
            if amount:
                update_blood_stock(blood_type, amount, "add", root)
        elif action == "deduct":
            amount = simpledialog.askinteger("Deduct Blood", f"Enter amount to deduct for {blood_type}:")
            if amount:
                cursor.execute("SELECT current_stock_ml FROM BLOODSTOCK WHERE blood_type = ?", (blood_type,))
                current_stock = cursor.fetchone()
                if current_stock and current_stock[0] >= amount:
                    # Update the database
                    update_blood_stock(blood_type, amount, "deduct", root)
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


def fetch_blood_stock():
    """Fetch current blood stock from the database."""
    try:
        connection = sqlite3.connect("blood_bank.db")  # Replace with your DB name
        cursor = connection.cursor()
        cursor.execute("SELECT blood_type, current_stock_ml FROM BLOODSTOCK")
        stock_data = cursor.fetchall()  # Returns a list of tuples (blood_type, stock)
        connection.close()
        return {blood_type: stock for blood_type, stock in stock_data}
    except sqlite3.Error as e:
        print(f"Error fetching blood stock: {e}")
        return {}

# Blood Stock Page UI
def bloodstock_ui():
    blood_stock = fetch_blood_stock()

    # Create the window
    root = ctk.CTk()
    root.title("Blood Stock Management")
    root.geometry("800x400")

    # Create a 4x2 grid of blood types
    for i, (blood_type,stock) in enumerate(blood_stock.items()):
        # Calculate row and column position for the 4x2 grid
        row = i // 4
        col = i % 4

        # Create a button with an image (if available) for each blood type
        button = ctk.CTkButton(root, text=f"{blood_type}\n{stock} mL", width=180, height=100,
                               command=lambda b=blood_type: open_update_window(b,root))

        # Place button in the grid
        button.grid(row=row, column=col, padx=10, pady=10)

    current_total_label = ctk.CTkLabel(root, text="Current Total: ", width=400, height=50, anchor="center", fg_color="#45818E")
    current_total_label.grid(row=4, column=0, columnspan=2, pady=10)

    # Row 5, Column 0 and 1 will be the "All-Time Total" label (spanning 2 columns)
    all_time_total_label = ctk.CTkLabel(root, text="All-Time Total: ", width=400, height=50, anchor="center", fg_color="#45818E")
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