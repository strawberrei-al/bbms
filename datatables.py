import sqlite3

# SQL Queries for table creation
sql_queries = [
    """
    CREATE TABLE IF NOT EXISTS LOGIN (
        username VARCHAR(50) PRIMARY KEY,
        password TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES USER(user_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS USER (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        bloodtype VARCHAR(3) NOT NULL,
        address TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS FORMDONATION (
        donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        bloodtype VARCHAR(3) NOT NULL,
        disease TEXT,
        donor_name VARCHAR,
        donation_date DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (user_id) REFERENCES USER(user_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS REQUESTBLOODFORM (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        bloodtype VARCHAR(3) NOT NULL,
        quantityneeded INTEGER NOT NULL,
        reason TEXT NOT NULL,
        patient_name VARCHAR,
        request_date DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (user_id) REFERENCES USER(user_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS BLOODSTOCK (
        blood_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        blood_type TEXT UNIQUE NOT NULL,
        current_stock_ml INTEGER DEFAULT 0,
        total_added_ml INTEGER DEFAULT 0
        );
    """,
    """
    CREATE TABLE IF NOT EXISTS NOTIFICATIONS (
        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        donation_id INTEGER,
        remarks TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES USERS(user_id)
    )
    """,
]

# Database connection function
def connect_db():
    return sqlite3.connect("blood_bank.db")

# Create or recreate tables
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Execute the other queries
    for query in sql_queries:
        cursor.execute(query)
    
    # cursor.execute("ALTER TABLE NOTIFICATIONS ADD COLUMN status TEXT DEFAULT 'unread';")

    # Insert the 8 standard blood types (only if the table is empty)
    # blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    # cursor.execute("INSERT INTO BLOODSTOCK (blood_type_id, blood_type,current_stock_ml,total_added_ml) VALUES ('1','A+','0','0')")
    # cursor.execute("INSERT INTO BLOODSTOCK (blood_type_id, blood_type,current_stock_ml,total_added_ml) VALUES ('2','A-','0','0')")
    # cursor.execute("INSERT INTO BLOODSTOCK (blood_type_id, blood_type,current_stock_ml,total_added_ml) VALUES ('3','B+','0','0')")
    # cursor.execute("INSERT INTO BLOODSTOCK (blood_type_id, blood_type,current_stock_ml,total_added_ml) VALUES ('4','B-','0','0')")
    # cursor.execute("INSERT INTO BLOODSTOCK (blood_type_id, blood_type,current_stock_ml,total_added_ml) VALUES ('5','AB+','0','0')")
    # cursor.execute("INSERT INTO BLOODSTOCK (blood_type_id, blood_type,current_stock_ml,total_added_ml) VALUES ('6','AB-','0','0')")
    # cursor.execute("INSERT INTO BLOODSTOCK (blood_type_id, blood_type,current_stock_ml,total_added_ml) VALUES ('7','O+','0','0')")
    # cursor.execute("INSERT INTO BLOODSTOCK (blood_type_id, blood_type,current_stock_ml,total_added_ml) VALUES ('8','O-','0','0')")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("it runs")

# Run the table creation function
create_tables()