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
