# api.py

from flask import Flask, request, jsonify
from bl.bl import SalaryManager
from datetime import date
import logging

# Initialize the Flask application
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create an instance of SalaryManager
salary_manager = SalaryManager()

# Root route for welcome message
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the WageWise API!"}), 200

# Route to get all employees
@app.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        employees = [emp.__dict__ for emp in salary_manager.get_employees()]
        return jsonify(employees), 200
    except Exception as e:
        logging.error(f"Error getting employees: {e}")
        return jsonify({"error": str(e)}), 500

# Route to get a specific employee by ID
@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    try:
        employee = salary_manager.get_employee_by_id(employee_id)
        if employee:
            return jsonify(employee.__dict__), 200
        else:
            return jsonify({"error": "Employee not found"}), 404
    except Exception as e:
        logging.error(f"Error getting employee {employee_id}: {e}")
        return jsonify({"error": str(e)}), 500

# Route to add a new employee
@app.route('/api/employees', methods=['POST'])
def add_employee():
    data = request.json
    try:
        salary_manager.add_employee(
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_hired=data['date_hired'],
            basic_salary=data['basic_salary']
        )
        return jsonify({"message": "Employee added successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error adding employee: {e}")
        return jsonify({"error": str(e)}), 500

# Route to update an existing employee
@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.json
    try:
        salary_manager.update_employee(
            employee_id,
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_hired=data['date_hired'],
            basic_salary=data['basic_salary']
        )
        return jsonify({"message": "Employee updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error updating employee {employee_id}: {e}")
        return jsonify({"error": str(e)}), 500

# Route to delete an employee
@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        salary_manager.delete_employee(employee_id)
        return jsonify({"message": "Employee deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting employee {employee_id}: {e}")
        return jsonify({"error": str(e)}), 500

# Route to record attendance for an employee
@app.route('/api/employees/<int:employee_id>/attendance', methods=['POST'])
def record_attendance(employee_id):
    data = request.json
    try:
        today = date.today()
        salary_manager.record_attendance(employee_id, str(today), data['status'], data['timestamp'])
        return jsonify({"message": "Attendance recorded successfully"}), 201
    except Exception as e:
        logging.error(f"Error recording attendance for employee {employee_id}: {e}")
        return jsonify({"error": str(e)}), 500

# Route to get attendance records for an employee
@app.route('/api/employees/<int:employee_id>/attendance', methods=['GET'])
def get_attendance_records(employee_id):
    try:
        records = salary_manager.get_attendance_records(employee_id)
        return jsonify(records), 200
    except Exception as e:
        logging.error(f"Error getting attendance records for employee {employee_id}: {e}")
        return jsonify({"error": str(e)}), 500

# Route to generate payroll for all employees
@app.route('/api/payroll', methods=['POST'])
def generate_payroll():
    try:
        success, message = salary_manager.generate_payroll_for_all()
        return jsonify({"message": message if success else "Error generating payroll"}), 200 if success else 500
    except Exception as e:
        logging.error(f"Error generating payroll: {e}")
        return jsonify({"error": str(e)}), 500

# Route to get the payroll of a specific employee
@app.route('/api/employees/<int:employee_id>/payroll', methods=['GET'])
def get_employee_payroll(employee_id):
    try:
        payroll_records = salary_manager.load_payroll(employee_id)
        return jsonify(payroll_records), 200
    except Exception as e:
        logging.error(f"Error getting payroll records for employee {employee_id}: {e}")
        return jsonify({"error": str(e)}), 500

# Route to handle favicon requests to avoid 404 errors
@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content

# Run the application
if __name__ == '__main__':
    app.run(debug=True)