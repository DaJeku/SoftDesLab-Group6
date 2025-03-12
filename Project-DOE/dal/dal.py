#dal.py
import sqlite3
import os
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the database file
current_dir = os.path.dirname(__file__)
DATABASE_FILE = os.path.join(current_dir, "payflow.db")

def create_connection():
    """Create a new database connection."""
    conn = sqlite3.connect(DATABASE_FILE)
    return conn

def initialize_db():
    """Initialize the database with the required tables."""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_hired DATE NOT NULL,
                basic_salary REAL NOT NULL,
                user_id INTEGER NOT NULL
            );
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                employee_id INTEGER NOT NULL,
                date DATE NOT NULL,
                status TEXT NOT NULL,
                time_logged TEXT NOT NULL,
                PRIMARY KEY (employee_id, date),
                FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
            );
        ''')
      
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                role TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            );
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payroll (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                date_generated DATE NOT NULL,
                payroll_period TEXT NOT NULL,
                attendance TEXT NOT NULL,  -- Format: "Present: 1, Late: 0, Absent: 0"
                average_work_hrs REAL NOT NULL,
                gross_pay REAL NOT NULL,
                income_tax REAL NOT NULL,
                annual_takehome_amount REAL NOT NULL,
                thirteenth_month_pay REAL NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
            );
        ''')
        
        conn.commit()
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize the database: {e}")
        raise RuntimeError(f"Failed to initialize the database: {e}")
    finally:
        conn.close()

# Attendance functions
def save_attendance(employee_id, date, status, timestamp):
    """Save employee attendance."""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO attendance (employee_id, date, status, time_logged)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(employee_id, date) DO UPDATE SET
            status = excluded.status,
            time_logged = excluded.time_logged
        ''', (employee_id, date, status, timestamp))
        conn.commit()
        logging.info(f"Attendance recorded for employee ID {employee_id} on {date} as {status} at {timestamp}.")
    except sqlite3.IntegrityError:
        logging.error(f"Integrity error while saving attendance for employee ID {employee_id} on {date}.")
        raise ValueError("Integrity constraint violated.")
    except Exception as e:
        logging.error(f"Failed to save attendance: {e}")
        raise RuntimeError(f"Failed to save attendance for employee {employee_id} on {date}.")
    finally:
        conn.close()

def load_attendance(employee_id):
    """Load attendance records for a specific employee."""
    attendance_records = []
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT date, status, time_logged FROM attendance WHERE employee_id=?", (employee_id,))
        rows = cursor.fetchall()
        for row in rows:
            attendance_records.append({
                "date": row[0],
                "status": row[1],
                "time": row[2]
            })
        logging.info(f"Loaded attendance records for employee ID {employee_id}.")
    except Exception as e:
        logging.error(f"Failed to load attendance records for employee {employee_id}: {e}")
        raise RuntimeError(f"Failed to load attendance records for employee {employee_id}.")
    finally:
        conn.close()
    
    return attendance_records

def load_accounts():
    """Load user accounts from the database."""
    accounts = {}
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.first_name, u.last_name, a.username, a.password, u.role 
            FROM users u 
            INNER JOIN admins a ON u.user_id = a.user_id
        """)
        rows = cursor.fetchall()
        for row in rows:
            accounts[row[2]] = (row[3], row[4])  # username maps to (password, role)
        logging.info("Loaded user accounts successfully.")
    except Exception as e:
        logging.error(f"Failed to load accounts due to: {e}")
        raise RuntimeError(f"Failed to load accounts due to: {e}")
    finally:
        conn.close()
    return accounts  

def save_account(username, password, first_name, last_name, role):
    """Save a new admin account into the database."""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (first_name, last_name, role) VALUES (?, ?, ?)
        ''', (first_name, last_name, role))
        user_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO admins (username, password, user_id)
            VALUES (?, ?, ?)
        ''', (username, password, user_id))

        conn.commit()
        logging.info(f"Account created for username: {username}")
    except sqlite3.IntegrityError:
        logging.error(f"Username {username} already exists.")
        raise ValueError("Username already exists.")
    except Exception as e:
        logging.error(f"Failed to save account {username} due to: {e}")
        raise RuntimeError(f"Failed to save account {username} due to: {e}")
    finally:
        conn.close()

def load_employees():
    """Load all employees from the database."""
    employees = []
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        for row in rows:
            employees.append({
                "employee_id": row[0],
                "username": row[1],
                "password": row[2],
                "first_name": row[3],
                "last_name": row[4],
                "date_hired": row[5],
                "basic_salary": row[6],
                "user_id": row[7]
            })
        logging.info("Loaded employees successfully.")
    except Exception as e:
        logging.error(f"Failed to load employees due to: {e}")
        raise RuntimeError(f"Failed to load employees due to: {e}")
    finally:
        conn.close()
    
    return employees

def save_employee(employee_id, username, password, first_name, last_name, date_hired, basic_salary, user_id):
    """Save or update an employee in the database."""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO employees (employee_id, username, password, first_name, last_name, date_hired, basic_salary, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET
            first_name = excluded.first_name,
            last_name = excluded.last_name,
            date_hired = excluded.date_hired,
            basic_salary = excluded.basic_salary
        ''', (employee_id, username, password, first_name, last_name, date_hired, basic_salary, user_id))
        conn.commit()
        logging.info(f"Employee {first_name} {last_name} saved or updated in the database.")
    except sqlite3.IntegrityError:
        logging.error(f"Duplicated username for {username}.")
        raise ValueError("Duplicated username.")
    except Exception as e:
        logging.error(f"Failed to save employee {first_name} {last_name} due to: {e}")
        raise RuntimeError(f"Failed to save employee {first_name} {last_name} due to: {e}")
    finally:
        conn.close()

def delete_employee(employee_id):
    """Delete an employee from the database."""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE employee_id=?", (employee_id,))
        if cursor.rowcount == 0:
            raise ValueError("Employee not found.")
        logging.info(f"Deleted employee with ID: {employee_id}")
        conn.commit()
    except Exception as e:
        logging.error(f"Failed to delete employee due to: {e}")
        raise RuntimeError(f"Failed to delete employee due to: {e}")
    finally:
        conn.close()

def save_payroll(employee_id, salary_date, payroll_period, attendance, average_work_hrs, gross_pay, income_tax, annual_takehome_amount, thirteenth_month_pay):
    """Save a payroll record for an employee."""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO payroll (employee_id, date_generated, payroll_period, attendance, average_work_hrs, gross_pay, income_tax, annual_takehome_amount, thirteenth_month_pay)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (employee_id, salary_date, payroll_period, attendance, average_work_hrs, gross_pay, income_tax, annual_takehome_amount, thirteenth_month_pay))
        conn.commit()
        logging.info("Payroll record saved successfully with Thirteenth Month Pay.")
    except Exception as e:
        logging.error(f"Failed to save payroll record: {e}")
        raise RuntimeError(f"Failed to save payroll record: {e}")
    finally:
        conn.close()

def load_payroll(employee_id):
    """Load payroll records for a specific employee."""
    payroll_records = []
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payroll WHERE employee_id=?", (employee_id,))
        rows = cursor.fetchall()
        for row in rows:
            payroll_records.append({
                "id": row[0],
                "employee_id": row[1],
                "date_generated": row[2],
                "payroll_period": row[3],
                "attendance": row[4],
                "average_work_hrs": row[5],
                "gross_pay": row[6],
                "income_tax": row[7],
                "annual_takehome_amount": row[8],
                "thirteenth_month_pay": row[9]
            })
        logging.info(f"Loaded payroll records for employee ID {employee_id}.")
    except Exception as e:
        logging.error(f"Failed to load payroll records: {e}")
        raise RuntimeError(f"Failed to load payroll records: {e}")
    finally:
        conn.close()
    
    return payroll_records

def clear_payroll():
    """Clear all entries from the payroll table."""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM payroll")
        conn.commit()
        logging.info("All entries in the payroll table have been cleared.")
    except Exception as e:
        logging.error(f"Failed to clear payroll table: {e}")
        raise RuntimeError(f"Failed to clear payroll table: {e}")
    finally:
        conn.close()

# Initialize the database and its tables
initialize_db()