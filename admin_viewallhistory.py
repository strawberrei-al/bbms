import sqlite3
import customtkinter as ctk
from tkinter import messagebox

def display_allhistory():
    """
    Displays the combined history of donations and requests in a new window for Admin.

    This will show all records from donations and requests in the database.
    """
    # Fetch all history (both donations and requests) from the database
    history = fetch_all_combined_history()  # You'll create a function to fetch all history
    if not history:
        ctk.CTkMessagebox.show_info("No History", "No history to display.")
        return

    # Create new window
    history_window = ctk.CTkToplevel()
    history_window.geometry("800x400")
    history_window.title("All History")

    # Frame for the table
    table_frame = ctk.CTkFrame(history_window, fg_color="white", corner_radius=10)
    table_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)  # Centered

    # Table headers
    headers = ["Type", "User ID", "Name", "Blood Type", "Detail", "Status", "Date"]
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(
            table_frame,
            text=header,
            font=("Arial", 14, "bold"),
            fg_color="#E8E8E8",
            anchor="center",
            width=20,
        )
        header_label.grid(row=0, column=col, padx=2, pady=2, sticky="nsew")

    # Add rows to the table
    for row, record in enumerate(history, start=1):
        for col, key in enumerate(headers):
            value = record[key]
            cell_label = ctk.CTkLabel(
                table_frame,
                text=value,
                font=("Arial", 12),
                anchor="center",
                width=20,
            )
            cell_label.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

    # Make columns expand
    for col in range(len(headers)):
        table_frame.grid_columnconfigure(col, weight=1)

def fetch_all_combined_history():
    """
    Fetches all donation and request history from the database.
    Returns a list of dictionaries with all the records.
    """
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    
    # Fetch donation history
    cursor.execute("""
        SELECT donation_id, user_id, donor_name, bloodtype, disease, status, donation_date
        FROM FORMDONATION
    """)
    donations = cursor.fetchall()

    # Fetch request history
    cursor.execute("""
        SELECT request_id, user_id, patient_name, bloodtype, quantityneeded, status, request_date
        FROM REQUESTBLOODFORM
    """)
    requests = cursor.fetchall()

    # Combine donations and requests into a single list of dictionaries
    combined_history = []
    
    # Combine donation history
    for donation in donations:
        combined_history.append({
            "Type": "Donation",
            "User ID": donation[1],
            "Name": donation[2],
            "Blood Type": donation[3],
            "Detail": f"Disease: {donation[4]}",
            "Status": donation[5],
            "Date": donation[6]
        })

    # Combine request history
    for request in requests:
        combined_history.append({
            "Type": "Request",
            "User ID": request[1],
            "Name": request[2],
            "Blood Type": request[3],
            "Detail": f"Quantity: {request[4]} ml",
            "Status": request[5],
            "Date": request[6]
        })

    conn.close()

    return combined_history