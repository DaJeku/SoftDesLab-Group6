"""
File: studenttest.py
Tests the Student class.
"""

from student import Student

def main():
    # Create a student with 5 scores
    student = Student("Alice", 5)
    
    # Set some scores
    student.setScore(1, 85)
    student.setScore(2, 90)
    student.setScore(3, 88)
    student.setScore(4, 92)
    student.setScore(5, 85)
    
    # Print the student's scores
    print("Student's scores:")
    print(student)
    
    # Test the new methods
    print("Mean:", student.getMean())
    print("Median:", student.getMedian())
    print("Mode:", student.getMode())
    print("Standard deviation:", student.getStd())
    
    # Add a new score
    student.addScore(95)
    print("\nAfter adding a new score:")
    print(student)
    
    # Delete a score
    student.deleteScore(2)
    print("\nAfter deleting the second score:")
    print(student)

if __name__ == "__main__":
    main()