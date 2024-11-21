import sqlite3
sql_queries = [
    """
    CREATE TABLE IF NOT EXIST LOGIN (
        username VARCHAR(50) PRIMARY KEY,
        password TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES USER(user_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXIST USER (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        bloodtype VARCHAR(3) NOT NULL,
        address TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    );
    """,
    """
    CREATE TABLE DONATIONFORM (
        donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        bloodtype VARCHAR(3) NOT NULL,
        disease TEXT,
        donation_date DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (user_id) REFERENCES USER(user_id)
    );
    """,
    """
    CREATE TABLE REQUESTFORM (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        bloodtype VARCHAR(3) NOT NULL,
        quantityneeded INTEGER NOT NULL,
        reason TEXT NOT NULL,
        request_date DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (user_id) REFERENCES USER(user_id)
    );
    """,
    """
    CREATE TABLE BLOODSTOCK (
        bloodstock_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bloodtype VARCHAR(3) NOT NULL,
        quantityeach INTEGER NOT NULL,
        totalquantity INTEGER NOT NULL,
        expiration_date DATE,
        donor_id INTEGER,
        FOREIGN KEY (donor_id) REFERENCES USER(user_id)
    );
    """
]

def connect_db():
# Connect to the database (creates a new file if it doesn't exist)
    return sqlite3.connect("blood_bank.db")

def create_tables():
# Create a cursor to execute SQL commands
    conn = connect_db()
    cursor = conn.cursor()

# Execute each query
    for query in sql_queries:
        cursor.execute(query)

# Commit changes and close the connection
    conn.commit()
    conn.close()

print("Tables created successfully!")
