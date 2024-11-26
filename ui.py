from tkinter import messagebox
import customtkinter as ctk
from PIL import Image  # Import PIL
from user_logic import register_user, login


def main_page():
    root = ctk.CTk()  # Create a new main window
    root.geometry("400x600")
    root.title("Blood Bank Manager")

    # Load the background image
    background_image = Image.open("background.png")
    background_image_ctk = ctk.CTkImage(background_image, size=(400, 600))

    # Adding Background Image to the Label
    background_label = ctk.CTkLabel(root, image=background_image_ctk, text="")
    background_label.pack(fill="both", expand=True)

    # Buttons
    user_login_button = ctk.CTkButton(root, text="User Login", command=lambda: user_login(root), corner_radius=20, bg_color="#FDDADA", fg_color="#8B0000", width=200, height=50)
    admin_login_button = ctk.CTkButton(root, text="Admin Login", command=lambda: admin_login(root), corner_radius=20, bg_color="#FDDADA", fg_color="#7B1818", width=200, height=50)
    register_button = ctk.CTkButton(root, text="Register", command=lambda: register_form(root), corner_radius=20, bg_color="#FDDADA", fg_color="#9A2A2A", width=200, height=50)

    # Button Placement
    user_login_button.place(relx=0.5, rely=0.4, anchor="center")
    admin_login_button.place(relx=0.5, rely=0.5, anchor="center")
    register_button.place(relx=0.5, rely=0.6, anchor="center")

    root.mainloop()


# Set up CustomTkinter appearance
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

def user_menu(user_id):
    from user_ui import donationform_ui, request_blood, display_history, notification

    import sqlite3  

    conn = sqlite3.connect("blood_bank.db") 
    cursor = conn.cursor()

    # Fetch the user's name using the user_id
    cursor.execute("SELECT name FROM USER WHERE user_id=?", (user_id,))
    user_name = cursor.fetchone()

    # Check if user exists
    if user_name:
        user_name = user_name[0]
    else:
        user_name = "User"

    menubackground_image = Image.open("menu_bg.png")
    menubackground_image_ctk = ctk.CTkImage(menubackground_image, size=(400, 600))

    logo_image = Image.open("logo.png")
    logo_image_resized = logo_image.resize((300, 100))  # Resize logo to 300x100 pixels
    logo_image_ctk = ctk.CTkImage(logo_image_resized, size=(300, 100))

    user_window = ctk.CTkToplevel()
    user_window.geometry("400x600")
    user_window.title("USER MENU")

    menubackground_label = ctk.CTkLabel(user_window, image=menubackground_image_ctk, text="")
    menubackground_label.pack(fill="both", expand=True)
    
    ctk.CTkLabel(user_window, text=f"Welcome,{user_name}!", font=("Arial", 20), bg_color="#FFF3F3").place(relx=0.5, rely=0.10, anchor="center")
    
    account_header = ctk.CTkLabel(user_window, text="Let’s create a world where\nblood is never in short supply.", font=("Arial", 18, "bold"), bg_color="#FFF3F3")
    account_header.place(relx=0.5, rely=0.18, anchor="center")

    donate_button = ctk.CTkButton(user_window, text="Donate Blood", command=lambda: donationform_ui(user_id), corner_radius=20, fg_color="#880808", width=200, height=50)
    request_button = ctk.CTkButton(user_window, text="Request Blood", command=lambda: request_blood(user_id), corner_radius=20, fg_color="#AA4A44", width=200, height=50)
    history_button = ctk.CTkButton(user_window, text="View History", command=lambda: display_history(user_id), corner_radius=20, fg_color="#6E260E", width=200, height=50)
    notif_button = ctk.CTkButton(user_window, text="Notification", command=lambda: notification(), corner_radius=20, fg_color="#E97451", width=200, height=50)
    logout_button = ctk.CTkButton(user_window, text="Logout", command=lambda: logout(user_window), corner_radius=20, fg_color="#EE4B2B", width=200, height=50)

    # Adding Background Image to the Label
    logo_label = ctk.CTkLabel(user_window, image=logo_image_ctk, text="", bg_color="#FFF3F3")
    logo_label.place(relx=0.5, rely=0.32, anchor="center")

    # Button Placement
    donate_button.place(relx=0.5, rely=0.46, anchor="center")
    request_button.place(relx=0.5, rely=0.56, anchor="center")
    history_button.place(relx=0.5, rely=0.66, anchor="center")
    notif_button.place(relx=0.5, rely=0.76, anchor="center")
    logout_button.place(relx=0.5, rely=0.86, anchor="center")


def admin_menu():
    admin_window = ctk.CTkToplevel()
    admin_window.geometry("400x600")
    admin_window.title("ADMIN MENU")
    
    ctk.CTkLabel(admin_window, text="Welcome, Admin!", font=("Arial", 20)).pack(pady=20)

def logout(user_window):
    user_window.destroy()
    main_page() # unsaon pagbalik sa mainpage (logins)


# Function for User Login Form (as an example)
def user_login(root):
    root.withdraw()
    login_form("User")

# Function for Admin Login Form (as an example)
def admin_login(root):
    root.withdraw()
    login_form("Admin")

# Function for Registration Form
def register_form():
    form_window = ctk.CTkToplevel()
    form_window.geometry("400x550")
    form_window.title("Register")

    # Title
    ctk.CTkLabel(form_window, text="Register", font=("Arial", 20)).pack(pady=10)

    account_header = ctk.CTkLabel(form_window, text="Account", font=("Arial", 18, "bold"))
    account_header.pack(pady=(10, 5))

    username_entry = ctk.CTkEntry(form_window, placeholder_text="Username")
    username_entry.pack(pady=5)
    pass_entry = ctk.CTkEntry(form_window, placeholder_text="Password", show="*")
    pass_entry.pack(pady=5)

    personal_details_header = ctk.CTkLabel(form_window, text="Personal Details", font=("Arial", 18, "bold"))
    personal_details_header.pack(pady=(20, 5))

    # Input Fields
    name_entry = ctk.CTkEntry(form_window, placeholder_text="Name")
    name_entry.pack(pady=5)
    age_entry = ctk.CTkEntry(form_window, placeholder_text="Age")
    age_entry.pack(pady=5)

    contact_entry = ctk.CTkEntry(form_window, placeholder_text="Phone number")
    contact_entry.pack(pady=5)
    email_entry = ctk.CTkEntry(form_window, placeholder_text="Email")
    email_entry.pack(pady=5)

    address_entry = ctk.CTkEntry(form_window, placeholder_text="Address")
    address_entry.pack(pady=5)

    # Dropdown for Blood Type
    blood_type = ctk.StringVar(value="Select Blood Type")
    blood_type_dropdown = ctk.CTkOptionMenu(
        form_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], variable=blood_type
    )
    blood_type_dropdown.pack(pady=5)

    # Submit Button
    def submit_registration():
        # Get Values
        name = name_entry.get()
        age = age_entry.get()
        address = address_entry.get()
        blood_type_value = blood_type.get()
        username = username_entry.get()
        password = pass_entry.get()
        contact = contact_entry.get()
        email = email_entry.get()

        # Validate Input
        if not name or not age or not address or not username or not password or not contact or not email or blood_type_value == "Select Blood Type":
            messagebox.showerror("Error", "Please fill out all fields!")
            return  # Exit the function if validation fails

        try:
            # Call the backend registration function
            register_user(name, age, blood_type_value, address, contact, email, username, password)
            messagebox.showinfo("Success", "Registration Successful!")
            form_window.destroy()  # Close the form window on success
        except Exception as e:
            messagebox.showerror("Error", "Registration failed: Please try again.")
            username_entry.delete(0, "end")
            pass_entry.delete(0, "end")
            name_entry.delete(0, "end")
            age_entry.delete(0, "end")
            address_entry.delete(0, "end")
            contact_entry.delete(0, "end")
            email_entry.delete(0, "end")
            blood_type.set("Select Blood Type")

    ctk.CTkButton(form_window, text="Submit", command=submit_registration).pack(pady=10)

# Function to Create Login Form (Reused for User/Admin)
def login_form(role):
    login_window = ctk.CTkToplevel()
    login_window.geometry("400x300")
    login_window.title(f"{role} Login")

    background_image = Image.open("userlogin.png")
    background_image_ctk = ctk.CTkImage(background_image, size=(400, 300))

    # Adding Background Image to the Label
    background_label = ctk.CTkLabel(login_window, image=background_image_ctk, text="")
    background_label.pack(fill="both", expand=True)

    # Input Fields
    username_entry = ctk.CTkEntry(login_window, placeholder_text="Username")
    username_entry.place(relx=0.5, rely=0.35, anchor="center", y=10)
    password_entry = ctk.CTkEntry(login_window, placeholder_text="Password", show="*")
    password_entry.place(relx=0.5, rely=0.45, anchor="center", y=10)

    # Submit Button
    def submit_login():
        username = username_entry.get()
        password = password_entry.get()

        try:
            # Call user_login from user_logic.py to validate credentials
            login_successful, user_role, user_id = login(username, password)

            if login_successful:
                if user_role.lower() == role.lower():  # Match role (case-insensitive)
                    # messagebox.showinfo("Success", f"{role} Login Successful!")
                    login_window.destroy()

                    # Direct to the respective menu
                    if role.lower() == "admin":
                        admin_menu()
                    elif role.lower() == "user":
                        user_menu(user_id)
                else:
                    messagebox.showerror("Error", f"This account is not a {role} account.")
                    username_entry.delete(0,"end")
                    password_entry.delete(0, "end")
            else:
                messagebox.showerror("Error", user_role)  # user_role contains the error message
                username_entry.delete(0,"end")
                password_entry.delete(0, "end")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            username_entry.delete(0,"end")
            password_entry.delete(0, "end")


    ctk.CTkButton(login_window, text="Submit", command=submit_login, fg_color="#D03D37").place(relx=0.5, rely=0.55, anchor="center", y=10)
