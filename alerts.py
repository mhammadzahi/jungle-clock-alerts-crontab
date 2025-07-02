# File: absent_employees.py
import psycopg2
from datetime import datetime
import pytz
from dotenv import load_dotenv
from send_email import send_alert_email
import os

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def get_absent_employees():
    try:
        # Connect to the database
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # Get today's date in Dubai timezone
        dubai_now = datetime.now(pytz.timezone("Asia/Dubai"))
        today = dubai_now.date()

        # Query: Get all employees whose "in" is NULL for today
        query = """
            SELECT e.admin_id, e.employee_id
            FROM employees e
            LEFT JOIN daily_reports dr 
                ON e.employee_id = dr.employee_id AND dr.date = %s
            WHERE dr."in" IS NULL
        """
        cur.execute(query, (today,))
        results = cur.fetchall()

        cur.close()
        conn.close()

        # Build the result dictionary
        absent_dict = {}
        for admin_id, employee_id in results:
            if admin_id not in absent_dict:
                absent_dict[admin_id] = []
            absent_dict[admin_id].append(employee_id)

        return absent_dict

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return {}


def get_admin_email(admin_id):
    try:
        # Connect to the database
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # Query: Get admin email by admin_id
        query = """
            SELECT email
            FROM admins
            WHERE id = %s
        """
        cur.execute(query, (admin_id,))
        result = cur.fetchone()

        cur.close()
        conn.close()

        if result:
            return result[0]
        return None

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

def get_employee_names(employee_ids):
    try:
        # Connect to the database
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # Query: Get employee names by employee_ids
        query = """
            SELECT name
            FROM employees
            WHERE id = ANY(%s)
        """
        cur.execute(query, (employee_ids,))
        results = cur.fetchall()

        cur.close()
        conn.close()

        # Extract names from the results
        return [row[0] for row in results]

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return []


if __name__ == "__main__":
    result = get_absent_employees()

    print(result)

    for admin_id, employee_ids in result.items():
        #to = get_admin_email(admin_id)
        #employee_names = get_employee_names(employee_ids)
        #send_alert_email(to, employee_names)
