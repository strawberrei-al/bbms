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
