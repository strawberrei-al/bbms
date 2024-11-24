from tkinter import messagebox
import customtkinter as ctk
from user_funtions import blood_donation

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
    pass


def view_history():
    pass


def notification():
    pass


def logout():
    pass # balik ra ni dayon sa login/register page

# diri ang mga ui guro, ayaw nalang sa ang functions.
# lahi na nga file ang functions. Pwede ra siya sa user_logic or what.