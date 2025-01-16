"""
File: student.py
Resources to manage a student's name and test scores.
"""
import random


class Student(object):
    """Represents a student."""

    def __init__(self, name, number):
        """All scores are initially 0."""
        self.name = name
        self.scores = []
        for count in range(number):
            self.scores.append(0)

    def getName(self):
        """Returns the student's name."""
        return self.name
  
    def setScore(self, i, score):
        """Resets the ith score, counting from 1."""
        self.scores[i - 1] = score

    def getScore(self, i):
        """Returns the ith score, counting from 1."""
        return self.scores[i - 1]
   
    def getAverage(self):
        """Returns the average score."""
        return sum(self.scores) / len(self.scores)
    
    def getHighScore(self):
        """Returns the highest score."""
        return max(self.scores)

    def __str__(self):
        """Returns the string representation of the student."""
        return "Name: " + self.name  + "\nScores: " + \
               " ".join(map(str, self.scores))

    def __eq__(self, other):
        """Tests for equality based on the student's name."""
        return self.name == other.name

    def __lt__(self, other):
        """Tests if this student's name is less than another's."""
        return self.name < other.name

    def __ge__(self, other):
        """Tests if this student's name is greater than or equal to another's."""
        return self.name >= other.name

def main():
    # Step 1: Create several Student objects with different names
    students = [
        Student("Charlie", 3),
        Student("Alice", 3),
        Student("Bob", 5),
        Student("David", 4),
        Student("Eve", 4)
    ]

    # Step 2: Shuffle the list of students
    random.shuffle(students)

    print("Students after shuffling:")
    for student in students:
        print(student)

    # Step 3: Sort the list
    students.sort()  # This will sort based on the __lt__ defined in Student class

    print("\nStudents after sorting by name:")
    for student in students:
        print(student)

if __name__ == "__main__":
    main()