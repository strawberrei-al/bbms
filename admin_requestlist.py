from tkinter import messagebox
import customtkinter as ctk
import sqlite3

def fetch_requests():
    # This function fetches the request data from the database
    try:
        conn = sqlite3.connect('blood_bank.db')
        cursor = conn.cursor()
        cursor.execute("SELECT request_id, user_id, bloodtype, quantityneeded, reason, request_date, patient_name, status FROM REQUESTBLOODFORM")
        requests = cursor.fetchall()
        conn.close()
        return requests
    except sqlite3.Error as e:
        print(f"Error fetching requests: {e}")
        return[]


def open_request_details(request):
    """Open the details page for the selected request."""
    request_id, user_id, bloodtype, quantityneeded, reason, request_date, patient_name, status = request

    # Creating a new window to show donation details
    details_window = ctk.CTkToplevel()
    details_window.title("Request Details")
    details_window.geometry("700x400")

    # Create a frame that will contain all the widgets, and center it
    main_frame = ctk.CTkFrame(details_window)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    # Configure the grid to expand in all directions
    details_window.grid_rowconfigure(0, weight=1)
    details_window.grid_columnconfigure(0, weight=1)

    main_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
    main_frame.grid_columnconfigure((0, 1), weight=1)

    # Add request details in a 4x2 grid layout
    ctk.CTkLabel(main_frame, text=f"Request ID: {request_id}", font=("Arial", 14)).grid(row=0, column=0, pady=5, padx=10, sticky="e")
    ctk.CTkLabel(main_frame, text=f"User ID: {user_id}", font=("Arial", 14)).grid(row=0, column=1, pady=5, padx=10, sticky="w")
    ctk.CTkLabel(main_frame, text=f"Patient Name: {patient_name}", font=("Arial", 14)).grid(row=1, column=0, pady=5, padx=10, sticky="e")
    ctk.CTkLabel(main_frame, text=f"Blood Type: {bloodtype}", font=("Arial", 14)).grid(row=1, column=1, pady=5, padx=10, sticky="w")
    ctk.CTkLabel(main_frame, text=f"Quantity (mL): {quantityneeded}", font=("Arial", 14)).grid(row=2, column=0, pady=5, padx=10, sticky="e")
    ctk.CTkLabel(main_frame, text=f"Reason: {reason}", font=("Arial", 14)).grid(row=2, column=1, pady=5, padx=10, sticky="w")
    ctk.CTkLabel(main_frame, text=f"Request Date: {request_date}", font=("Arial", 14)).grid(row=3, column=0, pady=5, padx=10, sticky="e")
    ctk.CTkLabel(main_frame, text=f"Status: {status}", font=("Arial", 14)).grid(row=3, column=1, pady=5, padx=10, sticky="w")

    # Remarks entry box
    remarks_entry = ctk.CTkTextbox(main_frame, width=500, height=100)
    remarks_entry.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")

    # Button frame
    button_frame = ctk.CTkFrame(main_frame)
    button_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

    # Configure the button frame
    button_frame.grid_columnconfigure((0, 1, 2), weight=1)

    # Buttons for Accept, Reject, and Return
    def send_response(action):
        """Send the admin's response to the user."""
        remarks = remarks_entry.get("1.0", "end").strip()  # Get text from the remarks field
        if not remarks:
            messagebox.showinfo("Remarks cannot be empty.")
            return
        
        try:
        # Update donation status in database
            conn = sqlite3.connect('blood_bank.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE REQUESTBLOODFORM SET status = ?, remarks = ? WHERE request_id = ?
            """, (action, remarks, request_id))

            # Insert a notification for the user
            cursor.execute("""
                INSERT INTO NOTIFICATIONS (user_id, request_id, remarks)
                VALUES (?, ?, ?)
            """, (user_id, request_id, remarks)) 

            conn.commit()
            print(f"Request {request_id} marked as {action}.")
        except sqlite3.Error as e:
            print(f"Error updating request: {e}")
        finally:
            conn.close()

        details_window.destroy()

    accept_button = ctk.CTkButton(button_frame, text="Accept", command=lambda: send_response("Accepted"))
    accept_button.grid(row=0, column=0, padx=10, pady=20)

    reject_button = ctk.CTkButton(button_frame, text="Place On Hold", command=lambda: send_response("On Hold"))
    reject_button.grid(row=0, column=1, padx=10, pady=20)

    return_button = ctk.CTkButton(button_frame, text="Return", command=details_window.destroy)
    return_button.grid(row=0, column=2, padx=10, pady=20)


def requests_ui():
    """Main request list page"""
    root = ctk.CTk()
    root.title("Request List")
    root.geometry("800x400")

    # Frame for Request List Table
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollable_frame = ctk.CTkScrollableFrame(main_frame)

    # Create column headers
    headers = ["Request ID", "User ID", "Blood Type", "Quantity(mL)", "Reason", "Request Date", "Patient Name", "Status"]
    for j, header in enumerate(headers):
        header_label = ctk.CTkLabel(scrollable_frame, text=header, font=("Arial", 12), anchor="w")
        header_label.grid(row=0, column=j, padx=10, pady=5)

    scrollable_frame.grid(row=1, column=0,columnspan=len(headers), sticky="nsew")

    # Populate the table with donation data
    requests = fetch_requests()
    for i, request in enumerate(requests):
        for j, value in enumerate(request):
            label = ctk.CTkLabel(scrollable_frame, text=str(value), anchor="w")
            label.grid(row=i + 1, column=j, padx=10, pady=5, sticky="w")

            # Add click event for each row
            label.bind("<Button-1>", lambda e, request=request: open_request_details(request))
    main_frame.grid_rowconfigure(1,weight=1)
    main_frame.grid_columnconfigure(0,weight=1)

    root.mainloop()

# requests_ui()