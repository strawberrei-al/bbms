import sqlite3
from tkinter import messagebox


def blood_donation(user_id, blood_type, donor_name, disease):
    """
    Inserts a new donation record into the database.

    Args:
        user_id (int): The ID of the user making the donation.
        blood_type (str): The blood type of the donor.
        donor_name (str): The name of the donor.
        disease (str): Any reported disease.
    """
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO FORMDONATION (user_id, bloodtype, donor_name, disease)
            VALUES (?, ?, ?, ?)
        """, (user_id, blood_type, donor_name, disease))
        conn.commit()
        messagebox.showinfo("Donation successfully recorded!")
    except Exception as e:
        messagebox.showerror(f"Error inserting donation data: {e}")
        conn.rollback()
    finally:
        conn.close()


def blood_request(user_id, blood_type, quantity, patient_name, reason):
    """
    Inserts a new donation record into the database.

    Args:
        user_id (int): The ID of the user making the request.
        blood_type (str): The blood type needed.
        quantity (int): Quantity needed in ml.
        patient_name (str): The name of the patient.
        reason (str): Any reported disease.
    """
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO REQUESTBLOODFORM (user_id, bloodtype, quantityneeded, reason, patient_name)
            VALUES (?, ?, ?, ?,?)
        """, (user_id, blood_type, quantity, reason, patient_name))
        conn.commit()
        messagebox.showinfo("Request successfully recorded!") #might remove later
    except Exception as e:
        messagebox.showerror(f"Error inserting request data: {e}") #also this
        conn.rollback()
    finally:
        conn.close()


def fetch_combined_history(user_id):
    """
    Fetches and displays combined history of donations and requests for a user.

    Args:
        user_id (int): The ID of the logged-in user.
    """
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()

    try:
        # Fetch donation history
        cursor.execute("""
            SELECT donor_name, bloodtype, disease, status, donation_date
            FROM FORMDONATION
            WHERE user_id = ?
        """, (user_id,))
        donations = cursor.fetchall()
        print(donations)

        # Fetch request history (add reason, date)
        cursor.execute("""
            SELECT patient_name, bloodtype, quantityneeded, status, request_date
            FROM REQUESTBLOODFORM
            WHERE user_id = ?
        """, (user_id,))
        requests = cursor.fetchall()

        # Combine and display histories
        combined_history = []

        for donation in donations:
            combined_history.append({
                "Type": "Donation",
                "Name": donation[0],
                "Blood Type": donation[1],
                "Detail": f"Disease: {donation[2]}",
                "Status": donation[3] if donation[3] else "Pending",
                "Date": donation[4],
            })

        for request in requests:
            combined_history.append({
                "Type": "Request",
                "Name": request[0],
                "Blood Type": request[1],
                "Detail": f"Quantity: {request[2]} ml",
                "Status": request[3] if request[3] else "Pending",
                "Date": request[4],
            })
        print(combined_history)

        return combined_history

    except Exception as e:
        print(f"Error fetching history: {e}")
    finally:
        conn.close()
