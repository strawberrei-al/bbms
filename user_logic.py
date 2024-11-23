import sqlite3
from tkinter import messagebox
import bcrypt
from datatables import connect_db  # Import the connect_db function to interact with the database


def register_user(name, age, bloodtype, address, username, password):
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()

    # Check if username already exists in LOGIN table
    cursor.execute("SELECT * FROM LOGIN WHERE username = ?", (username,))
    existing_user = cursor.fetchone()  # Fetch one result, if it exists

    if existing_user:
        messagebox.showerror("Error", "Username already exists!")
        
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Automatically assign 'user' role
    role = "user"

    # Insert into USER table
    cursor.execute("""
        INSERT INTO USER (name, age, bloodtype, address, role)
        VALUES (?, ?, ?, ?, ?)
    """, (name, age, bloodtype, address, role))

    user_id = cursor.lastrowid

    # Insert into LOGIN table
    cursor.execute("""
        INSERT INTO LOGIN (username, password, user_id)
        VALUES (?, ?, ?)
    """, (username, hashed_password.decode('utf-8'), user_id))

    conn.commit()
    print("User registration successful!")
    conn.close()


def user_login(username, password):
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    
        # Fetch stored hashed password and user_id for the username
    cursor.execute("SELECT password, user_id FROM LOGIN WHERE username = ?", (username,))
    record = cursor.fetchone()

    if record:
        stored_hashed_password, user_id = record

        # Compare the entered password with the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            # Fetch the user's role based on user_id
            cursor.execute("SELECT role FROM USER WHERE user_id = ?", (user_id,))
            role_record = cursor.fetchone()

            if role_record:
                role = role_record[0]
                conn.close()
                return True, role  # Login successful, return role
            else:
                conn.close()
                return False, "Role not found."  # No role associated with user_id
        else:
            conn.close()
            return False, "Incorrect password."  # Password mismatch
    else:
        conn.close()
        return False, "Username not found."  # No such username in the database
    
    