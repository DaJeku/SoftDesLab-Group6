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
            return(annual_income - 250000) * 0.15
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

