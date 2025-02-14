"""
File: studentapp.py
The application for editing and analyzing student scores.
"""

from student import Student
from studentview import StudentView

def main():
    # Create a student with 5 scores
    student = Student("Ken", 10)
    
    # Set some scores
    student.setScore(1, 85)
    student.setScore(2, 90)
    student.setScore(3, 88)
    student.setScore(4, 92)
    student.setScore(5, 85)
    student.setScore(6, 81)
    student.setScore(7, 79)
    student.setScore(8, 77)
    student.setScore(9, 75)
    student.setScore(10, 69)
    
    # Create the view and pass the student model
    view = StudentView(student)
    view.mainloop()

if __name__ == "__main__":
    main()
