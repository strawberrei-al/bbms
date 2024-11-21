import sqlite3
from datatables import connect_db  # Import the connect_db function to interact with the database

def register_user(username, password, name, age, blood_type, address, role):
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT * FROM login WHERE username=?", (username,))
    if cursor.fetchone():
        print("Username already exists!")
        return

    # Insert into the LOGIN table first (for authentication)
    cursor.execute("INSERT INTO login (username, password) VALUES (?, ?)", (username, password))

    # Insert into the USERS table with the same username
    cursor.execute("INSERT INTO users (username, name, age, blood_type, address, role) VALUES (?, ?, ?, ?, ?, ?)",
                   (username, name, age, blood_type, address, role))

    conn.commit()
    print("User registered successfully!")
    conn.close()
