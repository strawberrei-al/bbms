from tkinter import messagebox
import customtkinter as ctk
import sqlite3

def fetch_donations():
    # This function fetches the donation data from the database
    try:
        conn = sqlite3.connect('blood_bank.db')
        cursor = conn.cursor()
        cursor.execute("SELECT donation_id, user_id,bloodtype, disease, donation_date, donor_name, status FROM FORMDONATION")
        donations = cursor.fetchall()
        conn.close()
        return donations
    except sqlite3.Error as e:
        print(f"Error fetching donations: {e}")
        return[]


def open_donation_details(donation):
    """Open the details page for the selected donation."""
    donation_id, user_id, bloodtype, disease, donation_date, donor_name, status = donation

    # Creating a new window to show donation details
    details_window = ctk.CTkToplevel()
    details_window.title("Donation Details")
    details_window.geometry("600x400")

    # Create a frame that will contain all the widgets, and center it
    main_frame = ctk.CTkFrame(details_window)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    # Configure the grid to expand in all directions
    details_window.grid_rowconfigure(0, weight=1)
    details_window.grid_columnconfigure(0, weight=1)

# Create donation details labels inside the main frame
    ctk.CTkLabel(main_frame, text=" ", font=("Arial", 14)).grid(row=0, column=0)  # Blank cell
    ctk.CTkLabel(main_frame, text=f"Donation ID: {donation_id}", font=("Arial", 14)).grid(row=0, column=1, pady=5)
    ctk.CTkLabel(main_frame, text=" ", font=("Arial", 14)).grid(row=0, column=2)  # Blank cell

    ctk.CTkLabel(main_frame, text=f"User ID: {user_id}", font=("Arial", 14)).grid(row=1, column=0, pady=5)
    ctk.CTkLabel(main_frame, text=f"Donor Name: {donor_name}", font=("Arial", 14)).grid(row=1, column=1, pady=5)
    ctk.CTkLabel(main_frame, text=f"Blood Type: {bloodtype}", font=("Arial", 14)).grid(row=1, column=2, pady=5)

    ctk.CTkLabel(main_frame, text=f"Disease: {disease}", font=("Arial", 14)).grid(row=2, column=0, pady=5)
    ctk.CTkLabel(main_frame, text=f"Donation Date: {donation_date}", font=("Arial", 14)).grid(row=2, column=1, pady=5)
    ctk.CTkLabel(main_frame, text=f"Status: {status}", font=("Arial", 14)).grid(row=2, column=2, pady=5)

    # Remarks entry box
    remarks_entry = ctk.CTkTextbox(main_frame, width=400, height=100)
    remarks_entry.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")  # Centered and expanded

    # Configure rows and columns for expanding
    main_frame.grid_rowconfigure(3, weight=1)  # Make remarks entry stretch
    main_frame.grid_columnconfigure(0, weight=1)  # Make column 0 expand
    main_frame.grid_columnconfigure(1, weight=1)  # Make column 1 expand
    main_frame.grid_columnconfigure(2, weight=1)  # Make column 2 expand

    # Button Frame
    button_frame = ctk.CTkFrame(main_frame)
    button_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky="nsew")

    # Configure row and column in button_frame to expand
    button_frame.grid_rowconfigure(0, weight=1)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)

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
                UPDATE FORMDONATION SET status = ?, remarks = ? WHERE donation_id = ?
            """, (action, remarks, donation_id))

            # Insert a notification for the user
            cursor.execute("""
                INSERT INTO NOTIFICATIONS (user_id, donation_id, remarks)
                VALUES (?, ?, ?)
            """, (user_id, donation_id, remarks))  # Assuming `user_id` is available

            conn.commit()
            print(f"Donation {donation_id} marked as {action}.")
        except sqlite3.Error as e:
            print(f"Error updating donation: {e}")
        finally:
            conn.close()

        details_window.destroy()

    accept_button = ctk.CTkButton(button_frame, text="Accept", command=lambda: send_response("Accepted"))
    accept_button.grid(row=0, column=0, padx=10, pady=20)

    reject_button = ctk.CTkButton(button_frame, text="Reject", command=lambda: send_response("Rejected"))
    reject_button.grid(row=0, column=1, padx=10, pady=20)

    return_button = ctk.CTkButton(button_frame, text="Return", command=details_window.destroy)
    return_button.grid(row=0, column=2, padx=10, pady=20)


def donations_ui():
    """Main donation list page"""
    root = ctk.CTk(fg_color="#faf0e6")
    root.title("Donation List")
    root.geometry("800x400")

    # Frame for Donation List Table
    main_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=10)
    main_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)

    # Create column headers
    headers = ["Donation ID", "User ID", "Blood Type", "Disease", "Donation Date", "Donor Name", "   Status   "]
    for j, header in enumerate(headers):
        header_label = ctk.CTkLabel(
            main_frame, fg_color="#7c4848", text=header, text_color="white", font=("Arial", 14, "bold"), anchor="center", corner_radius=5
        )
        header_label.grid(row=0, column=j, padx=1, pady=1, sticky="nsew")

    # Configure column widths
    for column_index in range(len(headers)):
        main_frame.grid_columnconfigure(column_index, weight=1, minsize=100)  # Set a minimum size for alignment

    # Populate the table with donation data
    donations = fetch_donations()
    for i, donation in enumerate(donations):
        status = donation[-1]  # Assuming status is the last item
        for j, value in enumerate(donation):
            label = ctk.CTkLabel(
                main_frame,
                text=str(value),
                anchor="center",
                fg_color="#F0F0F0" if j == len(donation) - 1 and status != "Pending" else None,
                text_color="gray" if j == len(donation) - 1 and status != "Pending" else None,
                corner_radius=5,
            )
            label.grid(row=i + 1, column=j, padx=1, pady=1, sticky="nsew")

            # Only bind click event if the status is "Pending"
            if status == "Pending":
                label.bind("<Button-1>", lambda e, donation=donation: open_donation_details(donation))


    root.mainloop()


# donations_ui()