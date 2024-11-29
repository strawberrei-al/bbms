import sqlite3
import customtkinter as ctk
from tkinter import messagebox

def fetch_users():
    """
    Fetches all users from the database excluding the admin.
    
    Returns:
        list: A list of dictionaries containing user details.
    """
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    
    # Assuming the admin user can be identified by a specific ID or role.
    # For this example, we'll exclude users where role = 'Admin'.
    cursor.execute("""
        SELECT user_id, name, age, bloodtype, address, contact, email FROM USER WHERE role != 'Admin'
    """)
    users = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries for easier handling
    users_list = [{"User ID": user[0], "Name": user[1], "Age": user[2], "BloodType": user[3], "Address": user[4], "Contact": user[5], "Email": user[6]} for user in users]
    return users_list

def show_users():
    """
    Displays the list of users (excluding the admin) in a new window.
    """
    # Fetch the users
    users = fetch_users()
    
    if not users:
        ctk.messagebox.showinfo("No Users", "No users found.")
        return

    # Create a new window for the user list
    users_window = ctk.CTkToplevel()
    users_window.geometry("800x400")
    users_window.title("Users")

    table_frame = ctk.CTkFrame(users_window, fg_color="white", corner_radius=10)
    table_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)
    # Table headers

    headers = ["User ID", "Name", "Age","Blood Type","Address","Contact","Email", "Action"]
    for col, header in enumerate(headers):
        label = ctk.CTkLabel(
            table_frame, 
            text=header, 
            font=("Arial", 12, "bold"), 
            fg_color="#E8E8E8", 
            anchor="center", 
            width=20
            )
        label.grid(row=0, column=col, padx=2, pady=2, sticky="nsew")

    # Display the user rows
    for row, user in enumerate(users, start=1):
        for col, (key, value) in enumerate(user.items()):
            # value = user[key]
            label = ctk.CTkLabel(
                table_frame, 
                text=value, 
                font=("Arial", 12), 
                anchor="center", 
                width=20,
            )
            label.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

                # Add a delete button in the last column for each user
        delete_button = ctk.CTkButton(table_frame, text="Delete", command=lambda user_id=user["User ID"], window=users_window: delete_user(user_id, window))
        delete_button.grid(row=row, column=len(user), padx=5, pady=5)

    for col in range(len(headers)):
        table_frame.grid_columnconfigure(col,weight=1)


def delete_user(user_id, users_window):
    """
    Deletes a user from the database and refreshes the user list.
    
    Args:
        user_id (int): The ID of the user to delete.
        users_window (tk.Toplevel): The window that shows the user list.
    """
    # Confirm deletion
    confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user?")
    if not confirmation:
        return

    # Delete the user from the database
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM USER WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    # Close the current window and refresh the list
    users_window.destroy()
    show_users()  # Refresh the list