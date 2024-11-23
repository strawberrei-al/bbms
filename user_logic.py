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

    # Fetch the stored hashed password for the username
    cursor.execute("""SELECT password, user_id FROM LOGIN WHERE username = ?""", (username,))
    record = cursor.fetchone()

    if record:
        stored_hashed_password = record[0]
        user_id = record[1]

        # Compare the stored hashed password with the entered password
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            # Passwords match, now check the role
            cursor.execute("SELECT role FROM USER WHERE user_id = ?", (user_id,))
            role = cursor.fetchone()[0]

            if role == "user":
                print("User login successful!")
            else:
                print("This is not a user account.")
        else:
            print("Invalid credentials: incorrect password.")
    else:
        print("Invalid credentials: username not found.")

    conn.close()


def admin_login(username, password):
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()

    # Validate username and password
    cursor.execute("""
        SELECT user_id FROM LOGIN WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    if user:
        user_id = user[0]
        cursor.execute("SELECT role FROM USER WHERE user_id = ?", (user_id,))
        role = cursor.fetchone()[0]

        if role == "admin":
            print("Admin login successful!")
        else:
            print("This is not an admin account.")
    else:
        print("Invalid credentials.")

    conn.close()
    