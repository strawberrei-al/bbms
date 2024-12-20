import sqlite3
from tkinter import messagebox
from PIL import Image
import customtkinter as ctk
from user_functions import blood_donation, blood_request, fetch_combined_history

def donationform_ui(user_id):
    """
    UI for the Donate Blood form.
    Collects user input and passes it to the blood_donation function.
    
    Args:
        user_id (int): The ID of the currently logged-in user.
    """
    # Create the window
    window = ctk.CTkToplevel()
    window.geometry("400x400")
    window.title("Donate Blood")
    # ctk.CTkLabel(window, text="Donate Blood to Save a Life", font=("Arial", 20)).pack(pady=5)
    # Add the background image
    background_image = Image.open("bg_donationforms.png")  # Replace with your image path
    background_image_ctk = ctk.CTkImage(background_image, size=(400, 400))
    background_label = ctk.CTkLabel(window, image=background_image_ctk, text="")
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a frame on top of the background
    form_frame = ctk.CTkFrame(window, fg_color="white", corner_radius=10)  # Customize as needed
    form_frame.pack(expand=True, pady=20)  # Center the frame and add spacing

    # Input fields
    ctk.CTkLabel(form_frame, text="Blood Type:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    blood_type = ctk.CTkOptionMenu(form_frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], fg_color="#B25656")
    blood_type.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    ctk.CTkLabel(form_frame, text="Donor Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    donor_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter Donor Name")
    donor_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    ctk.CTkLabel(form_frame, text="Any Disease:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    disease_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter Disease (if any)")
    disease_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Submit button function
    def submit_donation():
        # Get data from input fields
        blood_type_value = blood_type.get()
        donor_name = donor_name_entry.get().strip()
        disease = disease_entry.get().strip()

        # Validation
        if not blood_type_value or not donor_name:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        try:
            # Call the backend function
            blood_donation(user_id, blood_type_value, donor_name, disease)
            messagebox.showinfo("Success", "Donation successfully recorded!")
            window.destroy()  # Close the form on success
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Submit button
    ctk.CTkButton(form_frame, text="Submit", fg_color="#B25656", command=submit_donation).grid(row=3, column=0, columnspan=2, pady=10)

def request_blood(user_id):
    """
    UI for the Request Blood form.
    Collects user input and passes it to the blood_request function.
    
    Args:
        user_id (int): The ID of the currently logged-in user.
    """
    # Create the window
    window = ctk.CTkToplevel(fg_color="white")
    window.geometry("400x400")
    window.title("Request Blood")

    background_image = Image.open("bg_requestform.png")  # Replace with your image path
    background_image_ctk = ctk.CTkImage(background_image, size=(400, 400))
    background_label = ctk.CTkLabel(window, image=background_image_ctk, text="")
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    form_frame = ctk.CTkFrame(window, fg_color="white", corner_radius=10)  # Customize as needed
    form_frame.pack(expand=True, pady=20)

    # Input fields
    ctk.CTkLabel(form_frame, text="Blood Type:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    blood_type = ctk.CTkOptionMenu(form_frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], fg_color="#B25656")
    blood_type.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    ctk.CTkLabel(form_frame, text="Quantity(ml):").grid(row=1, column=0, padx=10, pady=5, sticky="")
    quantity_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter Quantity Needed")
    quantity_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    ctk.CTkLabel(form_frame, text="Patient Name:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    patient_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter Patient Name")
    patient_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    ctk.CTkLabel(form_frame, text="Reason:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    reason_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter Reason for Request")
    reason_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Submit button function
    def submit_request():
        # Get data from input fields
        blood_type_value = blood_type.get()
        quantity = quantity_entry.get()
        patient_name = patient_name_entry.get().strip()
        reason = reason_entry.get().strip()

        # Validation
        if not blood_type_value or not quantity or not patient_name or not reason:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        try:
            # Call the backend function
            blood_request(user_id, blood_type_value, quantity, patient_name, reason)
            messagebox.showinfo("Success", "Request successfully sent!")
            window.destroy()  # Close the form on success
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Submit button
    ctk.CTkButton(form_frame, text="Submit", fg_color="#B25656", command=submit_request).grid(row=4, column=0, columnspan=2, pady=10)


def display_history(user_id):
    """
    Displays the combined history of donations and requests in a new window.

    Args:
        user_id (int): The ID of the user.
    """
    # Fetch history
    history = fetch_combined_history(user_id)
    if not history:
        messagebox.showinfo("No History", "No history to display.")
        return

    # Create new window
    history_window = ctk.CTkToplevel(fg_color="#faf0e6")
    history_window.geometry("800x400")
    history_window.title("Your History")

    # # Set background image (optional)
    # background_image = ctk.CTkImage(Image.open("background.png"), size=(800, 400))
    # bg_label = ctk.CTkLabel(history_window, image=background_image, text="")
    # bg_label.place(relwidth=1, relheight=1)

    # Frame for the table
    table_frame = ctk.CTkFrame(history_window, fg_color="white", corner_radius=10)
    table_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)  # Centered

    # Table headers
    headers = ["Type", "Name", "Blood Type", "Detail", "Status", "Date"]
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(
            table_frame,
            text=header,
            text_color="white",
            font=("Arial", 14, "bold"),
            fg_color="#ae0c00",
            corner_radius=5,
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

    # Add vertical and horizontal scrollbars (optional)
    # Scrollbars can improve navigation if you have a large history


def notification(user_id):
    def refresh_notifications():
        """Refreshes the notifications list in the table."""
        # Clear existing widgets in the table frame
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Reload notifications from the database
        conn = sqlite3.connect("blood_bank.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT notification_id, remarks, timestamp, status 
            FROM NOTIFICATIONS WHERE user_id = ?
        """, (user_id,))
        updated_notifications = cursor.fetchall()
        conn.close()

        if not updated_notifications:
            messagebox.showinfo("No Notifications", "You have no new notifications.")
            notif_window.destroy()
            return

        # Rebuild the table headers
        headers = ["ID", "Date", "Status", "Message"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"), anchor="center")
            label.grid(row=0, column=col, padx=10, pady=5)

        # Rebuild rows with updated data
        for row_idx, notif in enumerate(updated_notifications, start=1):
            notif_id, message, date, status = notif
            message_preview = message[:40] + "..." if len(message) > 40 else message

            ctk.CTkLabel(table_frame, text=notif_id, font=("Arial", 10), anchor="center").grid(row=row_idx, column=0, padx=10, pady=5)
            ctk.CTkLabel(table_frame, text=date, font=("Arial", 10), anchor="center").grid(row=row_idx, column=1, padx=10, pady=5)
            ctk.CTkLabel(table_frame, text=status, font=("Arial", 10), anchor="center").grid(row=row_idx, column=2, padx=10, pady=5)

            clickable_label = ctk.CTkLabel(table_frame, text=message_preview, font=("Arial", 10), anchor="w", cursor="hand2")
            clickable_label.grid(row=row_idx, column=3, padx=10, pady=5, sticky="w")
            clickable_label.bind("<Button-1>", lambda e, n_id=notif_id: open_notification_details(n_id, notif_window, refresh_notifications))

    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT notification_id, remarks, timestamp, status FROM NOTIFICATIONS WHERE user_id = ?
    """, (user_id,))
    notifications = cursor.fetchall()
    conn.close()

    if not notifications:
        messagebox.showinfo("No Notifications", "You have no new notifications.")
        return

    # Create a new window for notifications
    notif_window = ctk.CTkToplevel()
    notif_window.geometry("500x300")
    notif_window.title("Your Notifications")

    # Configure grid to center the table
    notif_window.grid_propagate(False)
    notif_window.grid_rowconfigure(0, weight=1)  # Top spacer
    notif_window.grid_rowconfigure(1, weight=0)  # Table content
    notif_window.grid_rowconfigure(2, weight=1)  # Bottom spacer
    notif_window.grid_columnconfigure(0, weight=1)  # Left spacer
    notif_window.grid_columnconfigure(1, weight=0)  # Table content
    notif_window.grid_columnconfigure(2, weight=1)  # Right spacer

    # Create a frame for the table
    table_frame = ctk.CTkFrame(notif_window, corner_radius=10)
    table_frame.grid(row=1, column=1, padx=20, pady=20)

    # Table headers
    headers = ["ID", "Date", "Status", "Message"]
    for col, header in enumerate(headers):
        label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"), anchor="center")
        label.grid(row=0, column=col, padx=10, pady=5)

    # Add rows to the table
    for row_idx, notif in enumerate(notifications, start=1):
        notif_id, message, date, status = notif

        # Truncated message for preview
        message_preview = message[:40] + "..." if len(message) > 40 else message

        # Add notification details to the table
        ctk.CTkLabel(table_frame, text=notif_id, font=("Arial", 10), anchor="center").grid(row=row_idx, column=0, padx=10, pady=5)
        ctk.CTkLabel(table_frame, text=date, font=("Arial", 10), anchor="center").grid(row=row_idx, column=1, padx=10, pady=5)
        ctk.CTkLabel(table_frame, text=status, font=("Arial", 10), anchor="center").grid(row=row_idx, column=2, padx=10, pady=5)

        # Clickable row for message preview
        clickable_label = ctk.CTkLabel(table_frame, text=message_preview, font=("Arial", 10), anchor="w", cursor="hand2")
        clickable_label.grid(row=row_idx, column=3, padx=10, pady=5, sticky="w")
        clickable_label.bind("<Button-1>", lambda e, n_id=notif_id: open_notification_details(n_id, notif_window))

    # Add "Delete All" button, aligned to the top-right of the table frame
    delete_all_button = ctk.CTkButton(table_frame, text="Delete All", command=lambda: delete_all_notifs(user_id), fg_color="#880808")
    delete_all_button.grid(row=0, column=len(headers) - 1, sticky="e", padx=5, pady=5)


def open_notification_details(notification_id, parent_window):

    parent_window.withdraw()

    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE NOTIFICATIONS
        SET status = 'read'
        WHERE notification_id = ?
    """, (notification_id,))
    conn.commit()

    # Fetch notification details
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT remarks, timestamp, status FROM NOTIFICATIONS WHERE notification_id = ?
    """, (notification_id,))
    notification = cursor.fetchone()
    conn.close()

    if not notification:
        messagebox.showerror("Error", "Notification not found.")
        return

    message, date, status = notification

    # Create a new window for the notification details
    detail_window = ctk.CTkToplevel()
    detail_window.geometry("500x300")
    detail_window.title("Notification Details")

    # Display details
    ctk.CTkLabel(detail_window, text=f"Date: {date}", font=("Arial", 12, "bold")).pack(pady=5)
    ctk.CTkLabel(detail_window, text=f"Status: {status}", font=("Arial", 12)).pack(pady=5)
    ctk.CTkLabel(detail_window, text="Message:", font=("Arial", 12, "bold")).pack(pady=5)

    # Justified format for the message
    message_text = ctk.CTkTextbox(detail_window, width=400, height=100, wrap="word")
    message_text.insert("1.0", message)
    message_text.configure(state="disabled")  # Make it read-only
    message_text.pack(pady=10)

    # Add Delete and Return buttons
    ctk.CTkButton(detail_window, text="Delete", command=lambda: delete_notification(notification_id, detail_window), fg_color="#880808").pack(side="left", padx=20, pady=10)
    ctk.CTkButton(detail_window, text="Return", command=lambda:(detail_window.destroy(), parent_window.deiconify()), fg_color="#6E260E").pack(side="right", padx=20, pady=10)


def delete_all_notifs(user_id):
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM NOTIFICATIONS WHERE user_id = ?", (user_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "All notifications deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete notifications: {e}")
        conn.rollback()
    finally:
        conn.close()


def delete_notification(notification_id, window):
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM NOTIFICATIONS WHERE notification_id = ?", (notification_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Notification deleted successfully.")
        window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete notification: {e}")
        conn.rollback()
    finally:
        conn.close()

# diri ang mga ui guro, ayaw nalang sa ang functions.
# lahi na nga file ang functions. Pwede ra siya sa user_logic or what.