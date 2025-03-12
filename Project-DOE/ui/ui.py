#ui.py
import flet as ft
from bl.bl import SalaryManager
import time
import calendar
import logging
from datetime import date, datetime

# Constants
FADE_STEP_DURATION = 0.02
FADE_STEPS = 100

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
salary_manager = SalaryManager()

def main(page: ft.Page):
    page.title = "PayFlow"
    page.bgcolor = ft.colors.BLUE_50
    
    def record_attendance(employee_id):
        try:
            today = date.today()
            existing_records = salary_manager.get_attendance_records(employee_id)
        
            if any(record['date'] == str(today) for record in existing_records):
                show_dialog("Error", "Attendance has already been recorded for today.")
                return

            current_time = datetime.now().time()
            late_time_in = datetime.strptime("9:15:00", "%H:%M:%S").time() # way past grace period
            time_off = datetime.strptime("17:00:00", "%H:%M:%S").time() # 5:00PM out
            
            if current_time <= late_time_in:
                status = "Present"
            elif current_time <= time_off:
                status = "Late"
            else:
                status = "Absent"
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            salary_manager.record_attendance(employee_id, today, status, timestamp)  
            show_dialog("Success", f"Attendance recorded as {status} for today at {timestamp}.")
        except Exception as e:
            show_dialog("Error", f"Failed to record attendance: {e}")

    def show_loading_message():
        fade_out_container = ft.Container(
            content=ft.Column(
                controls=[ft.Text("Loading...", color=ft.colors.WHITE, size=34)],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=ft.colors.GREEN_400,
            alignment=ft.alignment.center,
            padding=50,
            opacity=1
        )
        page.add(fade_out_container)
        page.update()
        for opacity in range(FADE_STEPS, -1, -1):
            fade_out_container.opacity = opacity / FADE_STEPS
            page.update()
            time.sleep(FADE_STEP_DURATION)

    def show_dialog(title, message):
        page.dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[ft.ElevatedButton(text="OK", on_click=lambda e: close_dialog())],
        )
        page.dialog.open = True
        page.update()

    def close_dialog():
        if page.dialog:
            page.dialog.open = False
            page.update()

    def welcome_screen():
        page.controls.clear()
        welcome_message = ft.Text("\nWelcome to PayFlow!", size=60, weight="bold", color=ft.colors.LIGHT_BLUE_400)
        description = ft.Text("Your trusted employee management system.", size=35, color=ft.colors.LIGHT_BLUE_400)
        start_button = ft.ElevatedButton(
            bgcolor=ft.colors.GREEN,
            text="Get Started",
            color=ft.colors.WHITE,
            on_click=lambda e: on_get_started(),
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=45, weight=ft.FontWeight.BOLD)),
            height=100, width=500,
        )
        page.add(ft.Container(content=ft.Column(
            controls=[welcome_message, description, start_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20),
            alignment=ft.alignment.center, padding=50))
        page.update()

    def on_get_started():
        show_loading_message()
        login_choice_screen()

    def login_choice_screen():
        page.controls.clear()
        title = ft.Text("PayFlow", size=60, weight="bold", color=ft.colors.LIGHT_BLUE_400)

        admin_login_button = ft.ElevatedButton(
            text="Login as Admin",
            on_click=lambda e: admin_login_screen(),
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            height=50,
            width=220,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
            ),
        )

        login_as_employee_button = ft.ElevatedButton(
            text="Login as Employee",
            on_click=lambda e: employee_login_screen(),
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
            height=50,
            width=240,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
            ),
        )

        page.add(ft.Container(
            content=ft.Column(
                controls=[title, admin_login_button, login_as_employee_button],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            alignment=ft.Alignment(0, 0),
            padding=50
        ))
        page.update()

    def admin_login_screen():
        page.controls.clear()
        admin_login_text = ft.Text("Admin Login", color=ft.colors.GREEN, size=45, weight=ft.FontWeight.BOLD)
        username_input = ft.TextField(label="Admin Username", color=ft.colors.BLACK)
        password_input = ft.TextField(label="Admin Password", password=True, color=ft.colors.BLACK)

        admin_login_button = ft.ElevatedButton(
            on_click=lambda e: admin_login_button_handler(username_input.value.strip(), password_input.value),
            bgcolor=ft.colors.GREEN,
            text="Login",
            color=ft.colors.WHITE,
            height=45,
            width=120,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
            ),
        )

        back_button = ft.ElevatedButton(
            text="Back",
            bgcolor=ft.colors.ORANGE,
            color=ft.colors.WHITE,
            height=45,
            width=100,
            on_click=lambda e: login_choice_screen(),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                alignment=ft.Alignment(0, 0),
            ),
        )

        page.add(ft.Container(
            content=ft.Column(
                controls=[admin_login_text, username_input, password_input, admin_login_button, back_button],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            alignment=ft.alignment.center,
            padding=50
        ))
        page.update()

    def admin_login_button_handler(username, password):
        try:
            if salary_manager.validate_login(username, password, "Admin"):
                logging.info(f"Admin user ({username}) logged in successfully.")
                salary_manager.set_current_user_id(username)
                salary_manager.current_admin_password = password
                employee_management_screen()
            else:
                show_dialog("Error", "Invalid admin username or password.")
        except Exception as ex:
            logging.error(f"Error during admin login for user: {username}. Exception: {ex}")
            show_dialog("Error", "An error occurred during admin login. Please try again.")

    def employee_management_screen():
        page.controls.clear()

        add_employee_button = ft.ElevatedButton(
            text="Create Employee Account",
            color=ft.colors.WHITE,
            on_click=lambda e: create_employee_account_screen(),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.LIGHT_BLUE,
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=5,
                text_style=ft.TextStyle(size=28, weight=ft.FontWeight.BOLD), alignment=ft.Alignment(0, 0)
            ),
            height=64,
            width=450,
        )

        create_admin_button = ft.ElevatedButton(
            text="Create Admin Account",
            color=ft.colors.WHITE,
            on_click=lambda e: create_admin_account_screen(),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.GREEN,
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=5,
                text_style=ft.TextStyle(size=28, weight=ft.FontWeight.BOLD), alignment=ft.Alignment(0, 0)
            ),
            height=64,
            width=450,
        )

        view_employee_button = ft.ElevatedButton(
            text="View Employee List",
            color=ft.colors.WHITE,
            on_click=lambda e: view_employee_list(),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.ORANGE_ACCENT_700,
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=5,
                text_style=ft.TextStyle(size=28, weight=ft.FontWeight.BOLD), alignment=ft.Alignment(0, 0)
            ),
            height=64,
            width=450,
        )

        generate_report_button = ft.ElevatedButton(
            text="Export Payroll Report .CSV",
            color=ft.colors.WHITE,
            on_click=lambda e: generate_payroll_report(),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.PURPLE_300,
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=5,
                text_style=ft.TextStyle(size=28, weight=ft.FontWeight.BOLD), alignment=ft.Alignment(0, 0)
            ),
            height=65,
            width=450,
        )

        generate_payroll_button = ft.ElevatedButton(
            text="Generate Payroll for All Employees",
            color=ft.colors.WHITE,
            on_click=lambda e: generate_payroll(),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.TEAL, 
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=5,
                text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD), alignment=ft.Alignment(0, 0)
            ),
            height=65,
            width=450,
        )

        delete_employee_button = ft.ElevatedButton(
            text="Delete Employee Account",
            color=ft.colors.WHITE,
            on_click=lambda e: delete_employee_screen(),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.RED,
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=5,
                text_style=ft.TextStyle(size=28, weight=ft.FontWeight.BOLD), alignment=ft.Alignment(0, 0)
            ),
            height=65,
            width=450,
        )

        incentives_button = ft.ElevatedButton(
            text="Salary Options",
            color=ft.colors.WHITE,
            on_click=lambda e: incentives_screen(),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.CYAN_500,
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=5,
                text_style=ft.TextStyle(size=28, weight=ft.FontWeight.BOLD), alignment=ft.Alignment(0, 0)
            ),
            height=65,
            width=450,
        )

        logout_button = ft.ElevatedButton(
            text="Logout",
            color=ft.colors.WHITE,
            on_click=lambda e: logout_admin(e),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.ORANGE,
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=5,
                text_style=ft.TextStyle(size=28, weight=ft.FontWeight.BOLD), alignment=ft.Alignment(0, 0)
            ),
            height=65,
            width=450,
        )

        button_container = ft.Row(
            controls=[
                ft.Container(content=add_employee_button, alignment=ft.alignment.center),
                ft.Container(content=create_admin_button, alignment=ft.alignment.center),
                ft.Container(content=view_employee_button, alignment=ft.alignment.center),
                ft.Container(content=generate_report_button, alignment=ft.alignment.center),
                ft.Container(content=generate_payroll_button, alignment=ft.alignment.center),
                ft.Container(content=incentives_button, alignment=ft.alignment.center),
                ft.Container(content=delete_employee_button, alignment=ft.alignment.center),
                ft.Container(content=logout_button, alignment=ft.alignment.center),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            wrap=True,
        )

        page.add(ft.Container(
            content=ft.Column(
                controls=[button_container], alignment=ft.MainAxisAlignment.CENTER, spacing=20
            ),
            alignment=ft.alignment.center,
            padding=50
        ))
        page.update()

    def generate_payroll():
        success, message = salary_manager.generate_payroll_for_all()
        if success:
            show_dialog("Success", message)
        else:
            show_dialog("Error", message)

    def create_employee_account_screen():
        page.controls.clear()        
        upper_text = ft.Text("Employee Details", size=30, weight="bold", color=ft.colors.BLUE)
        first_name_input = ft.TextField(label="First Name", color=ft.colors.BLACK)
        last_name_input = ft.TextField(label="Last Name", color=ft.colors.BLACK)
        username_input = ft.TextField(label="Username", color=ft.colors.BLACK)

        name_row = ft.Row(
            controls=[first_name_input, last_name_input, username_input],
            alignment=ft.MainAxisAlignment.START,
            spacing=10  
        )

        password_text = ft.Text("Enter and Confirm Password", size=30, weight="bold", color=ft.colors.BLUE)        
        password_input = ft.TextField(label="Password", password=True, color=ft.colors.BLACK)
        confirm_password_input = ft.TextField(label="Confirm Password", password=True, color=ft.colors.BLACK)        
        password_row = ft.Row(
            controls=[password_input, confirm_password_input],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )

        # Dropdowns
        current_year = datetime.now().year
        year_options = [str(year) for year in range(2010, current_year + 1)]  # Generate year options from 2010 to the current year
        month_options = [str(month).zfill(2) for month in range(1, 13)]  
        day_options = [str(day).zfill(2) for day in range(1, 32)]  

        space_drop = ft.Text("Employment Date", size=30, weight="bold", color=ft.colors.BLUE)
        year_dropdown = ft.Dropdown(label="Year", options=[ft.dropdown.Option(year) for year in year_options], bgcolor=ft.colors.WHITE70, color=ft.colors.BLACK)
        month_dropdown = ft.Dropdown(label="Month", options=[ft.dropdown.Option(month) for month in month_options], bgcolor=ft.colors.WHITE70, color=ft.colors.BLACK)
        day_dropdown = ft.Dropdown(label="Day", options=[ft.dropdown.Option(day) for day in day_options], bgcolor=ft.colors.WHITE70, color=ft.colors.BLACK)
    
        date_employed_row = ft.Row(
            controls=[year_dropdown, month_dropdown, day_dropdown],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )
        
        salary_text = ft.Text("Gross Salary", size=30, weight="bold", color=ft.colors.BLUE)
        salary_input = ft.TextField(label="Monthly Salary", keyboard_type=ft.KeyboardType.NUMBER, color=ft.colors.BLACK)
        message = ft.Text(color=ft.colors.BLACK)
        
        salary_row = ft.Row(
            controls=[salary_input],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )

        create_button = ft.ElevatedButton(
            text="Create Account",
            on_click=lambda e: create_employee_account_handler(
                first_name_input.value,
                last_name_input.value,
                f"{month_dropdown.value}/{day_dropdown.value}/{year_dropdown.value[-2:]}",  
                username_input.value,
                password_input.value,
                confirm_password_input.value,
                salary_input.value,
                message
            ),
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            height=60,
            width=170,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=27, weight=ft.FontWeight.BOLD), alignment=ft.Alignment(0, 0))
        )

        back_button = ft.ElevatedButton(
            bgcolor=ft.colors.ORANGE,
            color=ft.colors.WHITE,
            text="Back",
            height=60,
            width=80,
            on_click=lambda e: employee_management_screen(),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=27, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
            )
        )

        employee_creation_list_view = ft.ListView(
            controls=[
                ft.Container(
                    content=ft.Text("Create New Employee Account", size=50, weight="bold", color=ft.colors.GREEN),
                    alignment=ft.Alignment(0,0),
                    padding=ft.padding.only(bottom=43)
                ),
                upper_text,
                name_row,
                password_text,
                password_row,
                space_drop,
                date_employed_row,
                salary_text,
                salary_row,
                create_button,
                back_button,
                message
            ],
            spacing=10
        )

        page.add(employee_creation_list_view)
        page.update()

    def create_employee_account_handler(first_name, last_name, date_hired, username, password, confirm_password, salary, message):
        if password != confirm_password:
            message.value = "Passwords do not match."
            page.update()
            return

        if username and password and first_name and last_name and date_hired and salary:
            try:
                salary_manager.add_employee(username, password, first_name, last_name, date_hired, float(salary))
                message.value = f"Employee account '{username}' created successfully!"
                logging.info(f"Created employee account: {username}")
                time.sleep(2)
                create_employee_account_screen()
            except ValueError as ve:
                message.value = str(ve)
            except Exception as ex:
                logging.error(f"Error creating employee account: {ex}")
                message.value = "An error occurred while creating the account."
        else:
            message.value = "All fields are required."
        page.update()

    def view_attendance_records(employee_id):
        page.controls.clear()
        employee = salary_manager.get_employee_by_id(employee_id)
        records = salary_manager.get_attendance_records(employee_id)
        attendance_list_view = ft.ListView()
        
        for record in records:
            attendance_list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(f"Date: {record['date']} || Timed in: {record['time']}", color=ft.colors.BLACK),
                    subtitle=ft.Text(f"Status: {record['status']}", color=ft.colors.RED),
                )
            )

        back_button = ft.ElevatedButton(
            bgcolor=ft.colors.ORANGE,
            text="Back", color=ft.colors.WHITE,
            on_click=lambda e: show_employee_details(employee),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
            ),
        )

        page.add(ft.Container(content=ft.Column(controls=[attendance_list_view, back_button], alignment=ft.MainAxisAlignment.START, spacing=10), alignment=ft.alignment.center, padding=50))
        page.update()
    
    def employee_attendance_view(employee_id):
        page.controls.clear()
        records = salary_manager.get_attendance_records(employee_id)
        attendance_list_view = ft.ListView() 
        
        for record in records:
            attendance_list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(f"Date: {record['date']} || Timed in: {record['time']}", color=ft.colors.BLACK),
                    subtitle=ft.Text(f"Status: {record['status']}", color=ft.colors.RED),
                )
            )
        
        back_button = ft.ElevatedButton(
            bgcolor=ft.colors.ORANGE,
            text="Back", color=ft.colors.WHITE,
            on_click=lambda e: employee_info_page(salary_manager.get_employee_by_id(employee_id).username),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
            ),
        )

        page.add(ft.Container(content=ft.Column(controls=[attendance_list_view, back_button], alignment=ft.MainAxisAlignment.START, spacing=10), alignment=ft.alignment.center, padding=50))
        page.update()


    def create_admin_account_screen():
        page.controls.clear()

        username_input = ft.TextField(label="Admin Username", color=ft.colors.BLACK)
        password_input = ft.TextField(label="Admin Password", password=True, color=ft.colors.BLACK)
        confirm_password_input = ft.TextField(label="Confirm Password", password=True, color=ft.colors.BLACK)
        message = ft.Text(color=ft.colors.BLACK)

        create_button = ft.ElevatedButton(
            text="Create Admin Account",
            on_click=lambda e: create_admin_account_handler(
                username_input.value,
                password_input.value,
                confirm_password_input.value,
                message
            ),
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            height=50,
            width=270,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD), alignment=ft.Alignment(0, 0)),
        )

        back_button = ft.ElevatedButton(
            bgcolor=ft.colors.ORANGE,
            text="Back", color=ft.colors.WHITE,
            height=44,
            width=100,
            on_click=lambda e: employee_management_screen(),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
                alignment=ft.Alignment(0, 0)
            ),
        )

        page.add(ft.Column(
            controls=[
                ft.Text("Create New Admin Account", size=30, weight="bold", color=ft.colors.LIGHT_BLUE),
                username_input, password_input, confirm_password_input,
                create_button, back_button, message
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        ))

        page.update()

    def create_admin_account_handler(username, password, confirm_password, message):
        if password != confirm_password:
            message.value = "Passwords do not match."
            page.update()
            return

        if username and password:
            try:
                salary_manager.add_admin(username, password)
                message.value = f"Admin account '{username}' created successfully!"
                logging.info(f"Created admin account: {username}")
                time.sleep(2)
                employee_management_screen()
            except Exception as ex:
                logging.error(f"Error creating admin account: {ex}")
                message.value = "An error occurred while creating the account."
        else:
            message.value = "All fields are required."
        page.update()

    def view_employee_list(e=None):
        page.controls.clear()
        employee_list_view = ft.ListView()

        for emp in salary_manager.get_employees():
            employee_list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{emp.first_name} {emp.last_name} - Username: {emp.username}", color=ft.colors.BLACK),
                    subtitle=ft.Text(f"Monthly Salary: P{emp.basic_salary:.2f} | Date Hired: {emp.date_hired}", color=ft.colors.RED),
                    trailing=ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, emp=emp: show_update_dialog(emp)),
                    on_click=lambda e, emp=emp: show_employee_details(emp),
                )
            )
        
        clear_payroll_button = ft.ElevatedButton(
            bgcolor=ft.colors.RED,
            text="Clear all Payroll Records",
            color=ft.colors.WHITE,
            on_click=lambda e: confirm_clear_payroll(),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
            ),
        )   


        back_button = ft.ElevatedButton(
            bgcolor=ft.colors.ORANGE,
            text="Back", color=ft.colors.WHITE,
            on_click=lambda e: employee_management_screen(),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15), alignment=ft.Alignment(0, 0)
            ),
        )

        page.add(ft.Container(content=ft.Column(controls=[employee_list_view, clear_payroll_button, back_button], alignment=ft.MainAxisAlignment.START, spacing=10), alignment=ft.alignment.center, padding=50))
        page.update()
     
    def confirm_clear_payroll():
        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirm Clear Payroll"),
            content=ft.Text("Are you sure you want to clear all payroll records for all employees?"),
            actions=[
                ft.ElevatedButton(
                    text="Yes", 
                    on_click=lambda e: prompt_admin_payroll()
                ),
                ft.ElevatedButton(
                    text="No", 
                    on_click=lambda e: close_dialog()
                )
            ]
        )
        page.dialog.open = True
        page.update()

    def prompt_admin_payroll():
        password_input = ft.TextField(label="Admin Password", password=True, color=ft.colors.BLACK)

        dialog = ft.AlertDialog(
            title=ft.Text("Enter Admin Password"),
            content=ft.Column(controls=[password_input], spacing=10),
            actions=[
                ft.ElevatedButton(
                    text="Submit",
                    on_click=lambda e: verify_admin_payroll(password_input.value.strip())
                ),
                ft.ElevatedButton(
                    text="Cancel",
                    on_click=lambda e: close_dialog()
                )
            ]
        )
        page.dialog = dialog
        page.dialog.open = True
        page.update()

    def verify_admin_payroll(password):
        try:
            if salary_manager.current_admin_password and password == salary_manager.current_admin_password:
                clear_payroll_records()
                show_dialog("Success", "All payroll records have been cleared.")
            else:
                show_dialog("Error", "Incorrect password. Unable to clear payroll records.")
        except Exception as ex:
            show_dialog("Error", f"Failed to clear payroll records: {ex}")
            
    
    def clear_payroll_records():
        try:
            salary_manager.clear_payroll()
            logging.info("All payroll records cleared.")
            close_dialog()
        except Exception as ex:
            show_dialog("Error", f"Failed to clear payroll records: {ex}")   

    def generate_payroll_report():
        success, message = salary_manager.generate_payroll_report()
        if success:
            show_dialog("Success", f"Payroll report generated successfully at '{message}'!")
        else:
            show_dialog("Error", f"Failed to generate report: {message}")

    def show_update_dialog(employee):
        update_dialog = ft.AlertDialog(
            title=ft.Text("Update Employee Information"),
            content=ft.Column(
                controls=[
                    ft.TextField(label="First Name", value=employee.first_name, color=ft.colors.BLACK),
                    ft.TextField(label="Last Name", value=employee.last_name, color=ft.colors.BLACK),
                    ft.TextField(label="Date Hired (MM/DD/YY)", value=employee.date_hired, color=ft.colors.BLACK),
                    ft.TextField(label="Monthly Salary", value=str(employee.basic_salary), keyboard_type=ft.KeyboardType.NUMBER, color=ft.colors.BLACK),
                ],
                spacing=10,
            ),
            actions=[
                ft.ElevatedButton(text="Update", on_click=lambda e: handle_update(employee, update_dialog)),
                ft.ElevatedButton(text="Cancel", on_click=lambda e: close_dialog()),
            ],
        )
        page.dialog = update_dialog
        page.dialog.open = True
        page.update()

    def handle_update(employee, dialog):
        new_first_name = dialog.content.controls[0].value
        new_last_name = dialog.content.controls[1].value
        new_date_hired = dialog.content.controls[2].value
        new_salary = dialog.content.controls[3].value

        try:
            salary_manager.update_employee(employee.id, employee.username, new_first_name, new_last_name, new_date_hired, float(new_salary))
            show_dialog("Success", "Successfully Updated Employee Information.")
            view_employee_list()
        except ValueError as e:
            logging.error(f"Error updating employee: {e}")
            show_dialog("Error", "Please enter valid data.")
        except RuntimeError as e:
            logging.error(f"Data access error: {e}")
            show_dialog("Error", "An error occurred when accessing employee data.")

    def show_employee_details(employee):
        page.controls.clear()
        page.add(ft.Column(
            controls=[
                ft.Text(f"Employee: {employee.first_name} {employee.last_name}", size=30, weight="bold", color=ft.colors.RED),
                ft.Text(f"Username: {employee.username}", size=16, color=ft.colors.RED, weight=ft.FontWeight.BOLD),
                ft.Text(f"Date Employed: {employee.date_hired}", size=16, color=ft.colors.RED, weight=ft.FontWeight.BOLD),
                ft.Text(f"Monthly Salary: P{employee.basic_salary:.2f}", size=16, color=ft.colors.RED, weight=ft.FontWeight.BOLD),
                ft.Text(f"Thirteenth Month Pay: P{employee.thirteenth_month_pay:.2f}", size=16, color=ft.colors.RED, weight=ft.FontWeight.BOLD),
                ft.Text(f"Tax Deduction for Monthly Net Pay: P{(employee.tax)/12:.2f}", size=16, color=ft.colors.RED, weight=ft.FontWeight.BOLD),
                ft.Text(f"Monthly Net Pay: P{employee.basic_salary - (employee.tax/12):.2f}", size=16, color=ft.colors.RED, weight=ft.FontWeight.BOLD),
                # Check In and Check Out Buttons
                ft.ElevatedButton(
                    text="View Payroll",
                    on_click=lambda e: admin_view_payroll(employee.id, employee.username),
                    bgcolor=ft.colors.CYAN,
                    color=ft.colors.WHITE,
                    height=50,
                    width=200,
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))
                ),
                ft.ElevatedButton(
                    text="Mark as Absent",
                    on_click=lambda e: record_attendance(employee.id),
                    bgcolor=ft.colors.RED,
                    color=ft.colors.WHITE,
                    height=50,
                    width=200,
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))
                ),
                ft.ElevatedButton(
                    text="Attendance Record",
                    on_click=lambda e: view_attendance_records(employee.id),
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                    height=50,
                    width=200,
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ))
        
        back_button = ft.ElevatedButton(
            text="Back", 
            on_click=lambda e: view_employee_list(),
            bgcolor=ft.colors.ORANGE,
            color=ft.colors.WHITE,
            height=50, 
            width=200,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
            )
        )
        page.add(back_button)
        page.update()

    def view_emp_payroll(employee_id, username):
        page.controls.clear()

        # Load payroll records for the employee
        payroll_records = salary_manager.load_payroll(employee_id)

        # Create a DataTable with appropriate columns
        payroll_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Date Administered", color=ft.colors.LIGHT_BLUE)),
                ft.DataColumn(ft.Text("Gross Pay", color=ft.colors.LIGHT_BLUE)),
                ft.DataColumn(ft.Text("Attendance Record", color=ft.colors.LIGHT_BLUE)),
                ft.DataColumn(ft.Text("Income Tax", color=ft.colors.LIGHT_BLUE)),
                ft.DataColumn(ft.Text("Annual Take Home", color=ft.colors.LIGHT_BLUE)),
                ft.DataColumn(ft.Text("13th Month", color=ft.colors.LIGHT_BLUE)),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(record.get('date_generated', 'N/A'), color=ft.colors.ORANGE)),
                    ft.DataCell(ft.Text(f"P{record.get('gross_pay',0):.2f}", color=ft.colors.ORANGE)),
                    ft.DataCell(ft.Text(record.get('attendance', 'N/A'), color=ft.colors.ORANGE)),
                    ft.DataCell(ft.Text(f"P{record.get('income_tax'):.2f}", color=ft.colors.ORANGE)),
                    ft.DataCell(ft.Text(f"P{record.get('annual_takehome_amount'):.2f}", color=ft.colors.ORANGE)),
                    ft.DataCell(ft.Text(f"P{record.get('thirteenth_month_pay'):.2f}", color=ft.colors.ORANGE)),
                ])
                for record in payroll_records 
            ],
        )

        back_button = ft.ElevatedButton(
            bgcolor=ft.colors.ORANGE,
            text="Back", color=ft.colors.WHITE,
            on_click=lambda e: employee_info_page(username),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
            ),
        )

        # Add the payroll table and back button to the page
        page.add(ft.Container(content=ft.Column(controls=[payroll_table, back_button], alignment=ft.MainAxisAlignment.START, spacing=10), alignment=ft.alignment.center, padding=50))
        page.update()

    def admin_view_payroll(employee_id, username):
        page.controls.clear()

        # Load payroll records for the employee
        payroll_records = salary_manager.load_payroll(employee_id)

        # Create a DataTable with appropriate columns
        payroll_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Date Administered", color=ft.colors.RED)),
                ft.DataColumn(ft.Text("Gross Pay", color=ft.colors.RED)),
                ft.DataColumn(ft.Text("Attendance Record", color=ft.colors.RED)),
                ft.DataColumn(ft.Text("Income Tax", color=ft.colors.RED)),
                ft.DataColumn(ft.Text("Annual Take Home Pay", color=ft.colors.RED)),
                ft.DataColumn(ft.Text("13th Month", color=ft.colors.RED)),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(record.get('date_generated', 'N/A'), color=ft.colors.BROWN)),
                    ft.DataCell(ft.Text(f"P{record.get('gross_pay', 0):.2f}", color=ft.colors.BROWN)),
                    ft.DataCell(ft.Text(record.get('attendance', 'N/A'), color=ft.colors.BROWN)),
                    ft.DataCell(ft.Text(f"P{record.get('income_tax'):.2f}", color=ft.colors.BROWN)),
                    ft.DataCell(ft.Text(f"P{record.get('annual_takehome_amount'):.2f}", color=ft.colors.BROWN)),
                    ft.DataCell(ft.Text(f"P{record.get('thirteenth_month_pay'):.2f}", color=ft.colors.BROWN)),
                ])
                for record in payroll_records 
            ],
        )

        back_button = ft.ElevatedButton(
            bgcolor=ft.colors.ORANGE,
            text="Back", color=ft.colors.WHITE,
            on_click=lambda e:  show_employee_details(salary_manager.get_employee_by_id(employee_id)),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
            ),
        )

        page.add(ft.Container(content=ft.Column(controls=[payroll_table, back_button], alignment=ft.MainAxisAlignment.START, spacing=10), alignment=ft.alignment.center, padding=50))
        page.update()

    def logout_admin(e):
        page.controls.clear()
        logout_message = ft.Text("You have been logged out.", size=35, color=ft.colors.BLACK)
        back_to_login_button = ft.ElevatedButton(
            text="Back to Login", 
            on_click=lambda e: admin_login_screen(),
            bgcolor=ft.colors.ORANGE, 
            color=ft.colors.WHITE,
            height=50, 
            width=170,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=19, weight=ft.FontWeight.BOLD),
                alignment=ft.Alignment(0, 0)
            )
        )
        page.add(ft.Container(content=ft.Column(controls=[logout_message, back_to_login_button], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20), alignment=ft.alignment.center, padding=50))
        page.update()

    def logout_emp(e):
        page.controls.clear()
        logout_message = ft.Text("You have been logged out.", size=35, color=ft.colors.BLACK)
        back_to_login_button = ft.ElevatedButton(
            text="Back to Login", 
            on_click=lambda e: employee_login_screen(),
            bgcolor=ft.colors.ORANGE, 
            color=ft.colors.WHITE,
            height=50, 
            width=170,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=19, weight=ft.FontWeight.BOLD),
                alignment=ft.Alignment(0, 0)
            )
        )
        page.add(ft.Container(content=ft.Column(controls=[logout_message, back_to_login_button], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20), alignment=ft.alignment.center, padding=50))
        page.update()

    def employee_login_screen():
        page.controls.clear()
        emp_login_text = ft.Text("Employee Login", color=ft.colors.LIGHT_BLUE, size=45, weight=ft.FontWeight.BOLD)
        username_input = ft.TextField(label="Employee Username", color=ft.colors.BLACK)
        password_input = ft.TextField(label="Employee Password", password=True, color=ft.colors.BLACK)

        employee_login_button = ft.ElevatedButton(
            on_click=lambda e: employee_login_button_handler(username_input.value.strip(), password_input.value),
            bgcolor=ft.colors.LIGHT_BLUE,
            text="Login",
            color=ft.colors.WHITE,
            height=45,
            width=120,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
            ),
        )

        back_button = ft.ElevatedButton(
            text="Back",
            bgcolor=ft.colors.ORANGE,
            color=ft.colors.WHITE,
            height=45,
            width=100,
            on_click=lambda e: login_choice_screen(),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
            ),
        )

        page.add(ft.Container(
            content=ft.Column(
                controls=[emp_login_text, username_input, password_input, employee_login_button, back_button],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            alignment=ft.alignment.center,
            padding=50
        ))
        page.update()

    def employee_login_button_handler(username, password):
        try:
            if salary_manager.validate_login(username, password, "Employee"):
                logging.info(f"Employee user ({username}) logged in successfully.")
                employee = salary_manager.get_employee_by_username(username)
                salary_manager.set_current_user_id(employee.id)  # Set the current user ID
                employee_info_page(username)
            else:
                show_dialog("Error", "Invalid employee username or password.")
        except Exception as ex:
            logging.error(f"Error during employee login for user: {username}. Exception: {ex}")
            show_dialog("Error", "An error occurred during login. Please try again.")

    def employee_info_page(username):
        logging.info(f"Employee login attempt with username: {username}")

        employee = salary_manager.get_employee_by_username(username)
        if employee:
            logging.info(f"Employee data retrieved: {employee.first_name} {employee.last_name}")
            page.controls.clear()
            page.add(ft.Column(
                controls=[
                    ft.Text(f"Employee Name: {employee.first_name} {employee.last_name}", size=30, color=ft.colors.LIGHT_BLUE, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Username: {employee.username}", size=16, color=ft.colors.TEAL, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Date Employed: {employee.date_hired}", size=16, color=ft.colors.TEAL, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Monthly Take Home: P{employee.basic_salary - (employee.tax/12):.2f}", size=16, color=ft.colors.TEAL, weight=ft.FontWeight.BOLD),
                    
                    # Check In and Check Out Buttons
                    ft.ElevatedButton(
                        text="View Payroll",
                        on_click=lambda e: view_emp_payroll(employee.id, username),
                        bgcolor=ft.colors.CYAN,
                        color=ft.colors.WHITE,
                        height=50,
                        width=200,
                        style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))
                    ),                   
                    ft.ElevatedButton(
                        text="Time In",
                        on_click=lambda e: record_attendance(employee.id),
                        bgcolor=ft.colors.GREEN,
                        color=ft.colors.WHITE,
                        height=50,
                        width=200,
                        style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD))
                    ),
                    ft.ElevatedButton(
                        text="Attendance Record",
                        on_click=lambda e: employee_attendance_view(employee.id),
                        bgcolor=ft.colors.BLUE,
                        color=ft.colors.WHITE,
                        height=50,
                        width=200,
                        style=ft.ButtonStyle(text_style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD))
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ))
            back_button = ft.ElevatedButton(
                text="Logout",
                bgcolor=ft.colors.ORANGE,
                color=ft.colors.WHITE,
                height=50,
                width=200,
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD,),
                ),
                on_click=logout_emp
            )
            page.add(back_button)
            page.update()
        else:
            logging.warning(f"Employee not found for username: {username}")
            show_dialog("Error", "Employee not found. Please check your credentials.")

    def delete_employee_screen():
        page.controls.clear()
        employee_list_view = ft.ListView()

        for emp in salary_manager.get_employees():
            employee_list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{emp.first_name} {emp.last_name} - Username: {emp.username}", color=ft.colors.BLACK),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, emp=emp: confirm_delete_employee(emp)
                    ),
                )
            )

        back_button = ft.ElevatedButton(
            bgcolor=ft.colors.ORANGE,
            text="Back",
            color=ft.colors.WHITE,
            on_click=lambda e: employee_management_screen(),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
            ),
        )

        page.add(ft.Container(content=ft.Column(controls=[employee_list_view, back_button], alignment=ft.MainAxisAlignment.START, spacing=10), alignment=ft.alignment.center, padding=50))
        page.update()

    def confirm_delete_employee(employee):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirm Deletion"),
            content=ft.Text(f"Are you sure you want to delete employee {employee.first_name} {employee.last_name}?"),
            actions=[
                ft.ElevatedButton(
                    text="Yes", 
                    on_click=lambda e: prompt_emp_delete(employee)  
                ),
                ft.ElevatedButton(
                    text="No", 
                    on_click=lambda e: close_dialog()
                )
            ]
        )
        page.dialog.open = True
        page.update()

    def prompt_emp_delete(employee):
        password_input = ft.TextField(label="Admin Password", password=True, color=ft.colors.BLACK)

        dialog = ft.AlertDialog(
            title=ft.Text("Enter Admin Password"),
            content=ft.Column(controls=[password_input], spacing=10),
            actions=[
                ft.ElevatedButton(
                    text="Submit",
                    on_click=lambda e: verify_emp_delete(password_input.value.strip(), employee)
                ),
                ft.ElevatedButton(
                    text="Cancel",
                    on_click=lambda e: close_dialog()
                )
            ]
        )
        page.dialog = dialog
        page.dialog.open = True
        page.update()
        
    def verify_emp_delete(password, employee):
        try:
            if salary_manager.current_admin_password and password == salary_manager.current_admin_password:
                salary_manager.delete_employee(employee.id)
                show_dialog("Success", f"Successfully deleted employee: {employee.first_name} {employee.last_name}.")
                delete_employee_screen()
            else:
                show_dialog("Error", "Incorrect password. Unable to delete employee.")
        except Exception as ex:
            show_dialog("Error", f"Failed to delete employee: {ex}")
    
    def incentives_screen():
        page.controls.clear()
        employee_selector = ft.Dropdown(label="Select Employee", color=ft.colors.BLACK, options=[
            ft.dropdown.Option(emp.username) for emp in salary_manager.get_employees()
        ])
        
        attendance_input = ft.TextField(label="Number of Absent Days", keyboard_type=ft.KeyboardType.NUMBER, color=ft.colors.BLACK)
        overtime_input = ft.TextField(label="Number of Overtime Shifts (Max 5)", keyboard_type=ft.KeyboardType.NUMBER, color=ft.colors.BLACK)
        debt_input = ft.TextField(label="Debt Amount (if any)", keyboard_type=ft.KeyboardType.NUMBER, color=ft.colors.BLACK)

        message = ft.Text(color=ft.colors.BLACK)

        apply_button = ft.ElevatedButton(
            text="Apply Changes",
            on_click=lambda e: apply_incentives_handler(employee_selector.value, attendance_input.value, overtime_input.value, debt_input.value, message),
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            height=42,
            width=180,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
        )

        back_button = ft.ElevatedButton(
            text="Back",
            on_click=lambda e: employee_management_screen(),
            bgcolor=ft.colors.ORANGE,
            color=ft.colors.WHITE,
            height=42,
            width=90,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
            ),
        )

        page.add(ft.Column(
            controls=[
                ft.Text("Salary Options", size=30, color=ft.colors.CYAN_500, weight="bold"),
                employee_selector,
                attendance_input,
                overtime_input,
                debt_input,
                apply_button,
                back_button,
                message
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        ))

        page.update()

    def apply_incentives_handler(username, absent_days, overtime_shifts, debt_amount, message):
        try:
            absent_days = int(absent_days) if absent_days else 0
            overtime_shifts = int(overtime_shifts) if overtime_shifts else 0
            debt_amount = float(debt_amount) if debt_amount else 0.0

            employee = salary_manager.get_employee_by_username(username)

            if not employee: 
                message.value = "Employee not found."
                page.update()
                return

            # Calculate salary adjustments
            salary_deduction = employee.basic_salary * 0.01 * absent_days
            salary_increase = employee.basic_salary * 0.05 * min(overtime_shifts, 5)

            new_salary = employee.basic_salary - salary_deduction + salary_increase - debt_amount

            if new_salary < 0:
                message.value = "Salary cannot be negative."
            else:
                # Update the employee's salary
                salary_manager.update_employee(
                    employee.id,
                    employee.username,
                    employee.first_name,
                    employee.last_name,
                    employee.date_hired,
                    new_salary
                )

                employee.basic_salary = new_salary  # Update the in-memory representation
                message.value = f"New salary for {employee.first_name} {employee.last_name}: P{new_salary:.2f}"
                logging.info(f"Adjusted salary for {employee.first_name} {employee.last_name} to P{new_salary:.2f} after incentives.")

        except ValueError as e:
            message.value = "Please enter valid numeric inputs."
        except Exception as e:
            logging.error(f"Error applying incentives: {e}")
            message.value = "An error occurred while applying incentives."
        page.update()

    welcome_screen()

ft.app(target=main)