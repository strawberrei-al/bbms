from tkinter import messagebox, ttk
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
    ctk.CTkLabel(window, text="Donate Blood to Save a Life", font=("Arial", 20)).pack(pady=10)

    # Input fields
    ctk.CTkLabel(window, text="Blood Type:").pack(pady=5)
    blood_type = ctk.CTkOptionMenu(window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    blood_type.pack(pady=5)

    ctk.CTkLabel(window, text="Donor Name:").pack(pady=5)
    donor_name_entry = ctk.CTkEntry(window, placeholder_text="Enter Donor Name")
    donor_name_entry.pack(pady=5)

    ctk.CTkLabel(window, text="Any Disease:").pack(pady=5)
    disease_entry = ctk.CTkEntry(window, placeholder_text="Enter Disease (if any)")
    disease_entry.pack(pady=5)

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
    ctk.CTkButton(window, text="Submit", command=submit_donation).pack(pady=10)


def request_blood(user_id):
    """
    UI for the Request Blood form.
    Collects user input and passes it to the blood_request function.
    
    Args:
        user_id (int): The ID of the currently logged-in user.
    """
    # Create the window
    window = ctk.CTkToplevel()
    window.geometry("400x400")
    window.title("Request Blood")
    ctk.CTkLabel(window, text="We're here for you. Send us a Request!", font=("Arial", 20)).pack(pady=10)

    # Input fields
    ctk.CTkLabel(window, text="Blood Type:").pack(pady=5)
    blood_type = ctk.CTkOptionMenu(window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    blood_type.pack(pady=5)

    ctk.CTkLabel(window, text="Quantity(ml):").pack(pady=5)
    quantity_entry = ctk.CTkEntry(window, placeholder_text="Enter Quantity Needed")
    quantity_entry.pack(pady=5)

    ctk.CTkLabel(window, text="Patient Name:").pack(pady=5)
    patient_name_entry = ctk.CTkEntry(window, placeholder_text="Enter Patient Name")
    patient_name_entry.pack(pady=5)

    ctk.CTkLabel(window, text="Reason:").pack(pady=5)
    reason_entry = ctk.CTkEntry(window, placeholder_text="Enter Reason for Request")
    reason_entry.pack(pady=5)

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
    ctk.CTkButton(window, text="Submit", command=submit_request).pack(pady=10)


# def display_history(user_id):
#     """
#     Displays the combined history of donations and requests in a new window.

#     Args:
#         user_id (int): The ID of the user.
#     """
#     # Fetch history
#     history = fetch_combined_history(user_id)
#     if not history:
#         messagebox.showinfo("No History", "No history to display.")
#         return

# # Create new window
#     history_window = ctk.CTkToplevel()
#     history_window.geometry("600x400")
#     history_window.title("Your History")

# # Table headers
#     headers = ["Transaction Type", "Blood Type", "Name", "Disease", "Quantity", "Status", "Date"]
#     for col, header in enumerate(headers):
#         label = ctk.CTkLabel(history_window, text=header, font=("Arial", 12, "bold"))
#         label.grid(row=0, column=col, padx=5, pady=5)

#     # Add rows to the table
#     for row, record in enumerate(history, start=1):
#         for col, value in enumerate(record.values()):
#             label = ctk.CTkLabel(history_window, text=value, font=("Arial", 10))
#             label.grid(row=row, column=col, padx=5, pady=5)

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
    history_window = ctk.CTkToplevel()
    history_window.geometry("800x400")
    history_window.title("Your History")

    # Table headers
    headers = ["Type", "Name", "Blood Type", "Detail", "Status", "Date"]
    for col, header in enumerate(headers):
        label = ctk.CTkLabel(history_window, text=header, font=("Arial", 12, "bold"))
        label.grid(row=0, column=col, padx=5, pady=5)

    # Add rows to the table
    for row, record in enumerate(history, start=1):
        for col, key in enumerate(headers):
            value = record[key]  # Match keys to dictionary
            label = ctk.CTkLabel(history_window, text=value, font=("Arial", 10))
            label.grid(row=row, column=col, padx=5, pady=5)



def notification():
    pass


def logout():
    pass # balik ra ni dayon sa login/register page

# diri ang mga ui guro, ayaw nalang sa ang functions.
# lahi na nga file ang functions. Pwede ra siya sa user_logic or what.