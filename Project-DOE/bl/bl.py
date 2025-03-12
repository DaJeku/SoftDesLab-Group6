#bl.py
from dal.dal import load_employees, save_employee, delete_employee, save_account, load_accounts, save_payroll, load_payroll, save_attendance, load_attendance
import logging
import csv
import os
from datetime import date, timedelta

class Employee:
    def __init__(self, employee_id, username, password, first_name, last_name, date_hired, basic_salary, user_id):
        self.id = employee_id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.date_hired = date_hired
        self.basic_salary = basic_salary
        self.user_id = user_id
        self.tax = self.calculate_income_tax()
        self.thirteenth_month_pay = self.calculate_thirteenth_month_pay()
        
    def gross_pay(self):
        return self.basic_salary * 12

    def calculate_income_tax(self):
        annual_income = self.gross_pay()
        if annual_income <= 250000:
            return 0
        elif annual_income <= 400000:
            return (annual_income - 250000) * 0.15
        elif annual_income <= 800000:
            return 22500 + (annual_income - 400000) * 0.20
        elif annual_income <= 2000000:
            return 102500 + (annual_income - 800000) * 0.25
        elif annual_income <= 8000000:
            return 402500 + (annual_income - 2000000) * 0.30
        else:
            return annual_income * 0.35
        
    def calculate_thirteenth_month_pay(self):
        return (self.basic_salary * 12) / 12 if self.basic_salary > 0 else 0

    @classmethod
    def from_dict(cls, emp_dict):
        return cls(
            emp_dict['employee_id'], emp_dict['username'], emp_dict['password'],
            emp_dict['first_name'], emp_dict['last_name'],
            emp_dict['date_hired'], emp_dict['basic_salary'], emp_dict['user_id']
        )


class SalaryManager:
    def __init__(self):
        self.employees = [Employee.from_dict(emp) for emp in load_employees()]
        self.next_id = max([emp.id for emp in self.employees], default=0) + 1
        self.current_user_id = None  # Track the current user ID
        self.current_admin_password = None
        logging.info(f"Loaded {len(self.employees)} employees.")

    def record_attendance(self, employee_id, date, status, timestamp):
        save_attendance(employee_id, date, status, timestamp)
        logging.info(f"Attendance recorded for employee ID {employee_id} on {date} with status {status}.")
    
    def get_attendance_records(self, employee_id):
        records = load_attendance(employee_id)
        return [{"date": record[0], "time": record[1], "status": record[2]} for record in records]
    
    def set_current_user_id(self, user_id):
        self.current_user_id = user_id

    def get_current_user_id(self):
        return self.current_user_id

    def add_employee(self, username, password, first_name, last_name, date_hired, basic_salary):
        if self.username_exists(username):
            raise ValueError("Username already exists.")

        if not all([first_name, last_name, date_hired, username, password, basic_salary]):
            raise ValueError("All fields are required.")
        if basic_salary <= 0:
            raise ValueError("Basic salary must be greater than zero.")

        user_id = self.next_id  
        employee = Employee(self.next_id, username, password, first_name, last_name, date_hired, basic_salary, user_id)
        self.employees.append(employee)
        save_employee(employee.id, employee.username, employee.password, employee.first_name, employee.last_name, employee.date_hired, employee.basic_salary, user_id)
        logging.info(f"Employee {first_name} {last_name} added with ID {self.next_id}.")
        self.next_id += 1

    def add_admin(self, username, password):
        if self.username_exists(username):
            raise ValueError("Username already exists.")

        first_name = "Admin"
        last_name = "User"
        save_account(username, password, first_name, last_name, "Admin")
        logging.info(f"Admin account created for username: {username}")

    def username_exists(self, username):
        accounts = load_accounts()
        return username in accounts

    def validate_login(self, username, password, account_type):
        accounts = load_accounts()
        username = username.strip()

        if account_type.lower() == "admin":
            if username in accounts:
                stored_password, stored_account_type = accounts[username]
                if stored_password == password and stored_account_type.lower() == "admin":
                    logging.info(f"Admin login successful for username: {username}")
                    return True
                else:
                    logging.warning(f"Admin login failed for username: {username}: Invalid credentials.")
            logging.warning(f"Admin login failed for username: {username}: User does not exist.")
            return False

        if account_type.lower() == "employee":
            for emp in self.employees:
                if emp.username.strip().lower() == username.lower():
                    if emp.password == password:
                        logging.info(f"Employee login successful for username: {username}")
                        return True
                    else:
                        logging.warning(f"Employee login failed for username: {username}: Invalid credentials.")
            logging.warning(f"Employee login failed for username: {username}: User does not exist.")
            return False

        logging.warning(f"Login failed for username: {username}: Invalid account type provided.")
        return False

    def get_employees(self):
        logging.info(f"Retrieving {len(self.employees)} employees.")
        return self.employees

    def get_employee_by_username(self, username):
        username = username.strip()
        for emp in self.employees:
            if emp.username.strip() == username:
                logging.info(f"Employee found for username: {username}")
                return emp
        logging.warning(f"Employee not found for username: {username}")
        return None

    def get_employee_by_id(self, employee_id):
        for emp in self.employees:
            if emp.id == employee_id:
                return emp
        return None

    def update_employee(self, employee_id, username, first_name, last_name, date_hired, basic_salary):
        for emp in self.employees:
            if emp.id == employee_id:
                emp.username = username
                emp.first_name = first_name
                emp.last_name = last_name
                emp.date_hired = date_hired
                emp.basic_salary = basic_salary
                
                save_employee(emp.id, emp.username, emp.password, emp.first_name, emp.last_name, emp.date_hired, emp.basic_salary, emp.user_id)
                logging.info(f"Updated employee ID {employee_id} to {first_name} {last_name}.")
                return

        raise ValueError("Employee not found.")

    def delete_employee(self, employee_id):
        if employee_id is None:
            raise ValueError("Employee ID must be provided.")

        self.employees = [emp for emp in self.employees if emp.id != employee_id]
        
        try:
            delete_employee(employee_id)
            logging.info(f"Deleted employee ID {employee_id}.")
        except Exception as e:
            logging.error(f"Error deleting employee with ID {employee_id}: {e}")
            raise RuntimeError(f"Failed to delete employee: {e}")

    def generate_payroll_report(self):
        report_filename = 'payroll_report.csv'
        report_path = os.path.join(os.getcwd(), report_filename)
        
        try:
            report_data = []
            for emp in self.get_employees():
                payroll_records = self.load_payroll(emp.id)
                for record in payroll_records:
                    report_data.append({
                        "Employee ID": emp.id,
                        "Employee Name": f"{emp.first_name} {emp.last_name}",
                        "Date Generated": record['date_generated'],
                        "Payroll Period": record['payroll_period'],
                        "Attendance": record['attendance'],
                        "Average Work Hours": record['average_work_hrs'],
                        "Gross Pay": record['gross_pay'],
                        "Income Tax": record['income_tax'],
                        "Annual Take Home": record['annual_takehome_amount'],
                        "13th Month": record['thirteenth_month_pay'],
                    })

            with open(report_path, 'w', newline='') as csv_file:
                if report_data:
                    fieldnames = report_data[0].keys()
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                    writer.writeheader()

                    for row in report_data:
                        writer.writerow(row)

            return True, report_path
        except Exception as e:
            logging.error(f"Failed to generate payroll report: {e}")
            return False, str(e)

    def load_payroll(self, employee_id):
        return load_payroll(employee_id)

    def save_payroll(self, employee_id, salary_date, payroll_period, attendance, average_work_hrs, gross_pay, income_tax, annual_takehome_amount, thirteenth_month_pay):
        save_payroll(
            employee_id, 
            salary_date, 
            payroll_period, 
            attendance, 
            average_work_hrs, 
            gross_pay, 
            income_tax, 
            annual_takehome_amount, 
            thirteenth_month_pay,
        )

    def generate_employee_payroll(self, employee_id, salary_date, payroll_period_start, payroll_period_end):
        employee = self.get_employee_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        attendance_records = self.get_attendance_records(employee_id)

        # Attendance
        present_days = sum(1 for record in attendance_records if record['status'] == "Present")
        late_days = sum(1 for record in attendance_records if record['status'] == "Late")
        absent_days = sum(1 for record in attendance_records if record['status'] == "Absent")

        attendance = f"Present: {present_days}, Late: {late_days}, Absent: {absent_days}"

        average_work_hours = (present_days + late_days) * 8  # Assuming 8 hours per day
        
        thirteenth_month_pay = employee.calculate_thirteenth_month_pay()

        gross_pay = (employee.basic_salary * 12) + thirteenth_month_pay
        
        income_tax = employee.calculate_income_tax()
         
        annual_takehome_amount = gross_pay - income_tax 

        self.save_payroll(
            employee_id, 
            salary_date, 
            f"{payroll_period_start} to {payroll_period_end}",  # Correct payroll period
            attendance, 
            average_work_hours, 
            gross_pay, 
            income_tax, 
            annual_takehome_amount, 
            thirteenth_month_pay,
        )
        logging.info(f"Payroll generated for {employee.first_name} {employee.last_name} for the period {payroll_period_start} to {payroll_period_end}.")

    def generate_payroll_for_all(self):
        payroll_date = date.today().strftime("%Y-%m-%d")
        payroll_period_start = (date.today().replace(day=1) - timedelta(days=1)).replace(day=1).strftime("%Y-%m-%d")
        payroll_period_end = (date.today().replace(day=1) - timedelta(days=1)).strftime("%Y-%m-%d")

        try:
            for emp in self.get_employees():
                self.generate_employee_payroll(emp.id, payroll_date, payroll_period_start, payroll_period_end)
            return True, "Payroll records generated for all employees."
        except Exception as e:
            logging.error(f"Failed to generate payroll for all employees: {e}")
            return False, str(e)

    def get_attendance_records(self, employee_id):
        return load_attendance(employee_id)

    def clear_payroll(self):
        """Clear all entries from the payroll table."""
        logging.info("Clearing all payroll records.")
        from dal.dal import clear_payroll
        clear_payroll()
