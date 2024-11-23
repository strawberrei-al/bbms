from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk  # Import PIL

# Set up CustomTkinter appearance
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Main Application Window
root = ctk.CTk()
root.geometry("400x600")
root.title("Blood Bank Manager")

# Load the background image using Pillow
background_image = Image.open("background.jpg")  # Open the image using Pillow
background_image = background_image.resize((400, 600))  # Resize it to fit the window

# Convert the image to a format CustomTkinter can use
background_image_tk = ImageTk.PhotoImage(background_image)

# Adding Background Image to the Label
background_label = ctk.CTkLabel(root, image=background_image_tk, text="")
background_label.place(relwidth=1, relheight=1)

# Function for User Login Form (as an example)
def user_login():
    login_form("User")

# Function for Admin Login Form (as an example)
def admin_login():
    login_form("Admin")

# Function for Registration Form
def register_form():
    form_window = ctk.CTkToplevel(root)
    form_window.geometry("400x500")
    form_window.title("Register")

    # Title
    ctk.CTkLabel(form_window, text="Register", font=("Arial", 20)).pack(pady=10)

    # Input Fields
    name_entry = ctk.CTkEntry(form_window, placeholder_text="Name")
    name_entry.pack(pady=10)
    age_entry = ctk.CTkEntry(form_window, placeholder_text="Age")
    age_entry.pack(pady=10)
    address_entry = ctk.CTkEntry(form_window, placeholder_text="Address")
    address_entry.pack(pady=10)

    # Dropdown for Blood Type
    blood_type = ctk.StringVar(value="Select Blood Type")
    blood_type_dropdown = ctk.CTkOptionMenu(
        form_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], variable=blood_type
    )
    blood_type_dropdown.pack(pady=10)

    # Submit Button
    def submit_registration():
        # Get Values
        name = name_entry.get()
        age = age_entry.get()
        address = address_entry.get()
        blood_type_value = blood_type.get()

        # Validate Input
        if not name or not age or not address or not blood_type_value == "Select Blood Type":
            messagebox.showerror("Error", "Please fill out all fields!")
        else:
            messagebox.showinfo("Success", "Registration Successful!")
            form_window.destroy()

    ctk.CTkButton(form_window, text="Submit", command=submit_registration).pack(pady=10)

# Function to Create Login Form (Reused for User/Admin)
def login_form(role):
    login_window = ctk.CTkToplevel(root)
    login_window.geometry("400x300")
    login_window.title(f"{role} Login")

    # Title
    ctk.CTkLabel(login_window, text=f"{role} Login", font=("Arial", 20)).pack(pady=10)

    # Input Fields
    username_entry = ctk.CTkEntry(login_window, placeholder_text="Username")
    username_entry.pack(pady=10)
    password_entry = ctk.CTkEntry(login_window, placeholder_text="Password", show="*")
    password_entry.pack(pady=10)

    # Submit Button
    def submit_login():
        username = username_entry.get()
        password = password_entry.get()

        # Mock Login Check
        if username == "admin" and password == "1234" and role == "Admin":
            messagebox.showinfo("Success", "Admin Login Successful!")
            login_window.destroy()
        elif username == "user" and password == "1234" and role == "User":
            messagebox.showinfo("Success", "User Login Successful!")
            login_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid Credentials!")
            username_entry.delete(0, "end")
            password_entry.delete(0, "end")

    ctk.CTkButton(login_window, text="Submit", command=submit_login).pack(pady=10)


# Adding Buttons to Main Page
user_login_button = ctk.CTkButton(root, text="User Login", command=user_login, corner_radius=20, fg_color="#1E90FF", width=200, height=50)
admin_login_button = ctk.CTkButton(root, text="Admin Login", command=admin_login, corner_radius=20, fg_color="#32CD32", width=200, height=50)
register_button = ctk.CTkButton(root, text="Register", command=register_form, corner_radius=20, fg_color="#FFA07A", width=200, height=50)

# Button Placement
user_login_button.place(relx=0.5, rely=0.4, anchor="center")
admin_login_button.place(relx=0.5, rely=0.5, anchor="center")
register_button.place(relx=0.5, rely=0.6, anchor="center")

root.mainloop()
