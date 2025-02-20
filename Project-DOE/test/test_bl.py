#test_bl.py
import unittest
from unittest.mock import patch, MagicMock
from bl import Employee, SalaryManager

class TestEmployee(unittest.TestCase):
    
    def setUp(self):
        # Sample employee data for testing
        self.emp_data = {
            'employee_id': 1,
            'username': 'john_doe',
            'password': 'secret',
            'first_name': 'John',
            'last_name': 'Doe',
            'date_hired': '2023-01-01',
            'basic_salary': 30000,
            'user_id': 1
        }
        self.employee = Employee.from_dict(self.emp_data)

    def test_employee_creation(self):
        self.assertEqual(self.employee.first_name, 'John')
        self.assertEqual(self.employee.last_name, 'Doe')
        self.assertEqual(self.employee.calculate_tax(30000), 6000)

    def test_calculate_thirteenth_month_pay(self):
        self.assertEqual(self.employee.calculate_thirteenth_month_pay(), 2500)
        
    def test_calculate_tax(self):
        self.assertEqual(self.employee.calculate_tax(30000), 6000)  # 20% of 30000
        self.assertEqual(self.employee.calculate_tax(60000), 18000)  # 30% of 60000


if __name__ == '__main__':
    unittest.main()