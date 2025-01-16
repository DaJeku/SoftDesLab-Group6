"""
File: student.py
Resources to manage a student's name and test scores.
"""

class Student(object):
    """Represents a student."""

    def __init__(self, name, number):
        """Initializes the student's name and test scores."""
        self.name = name
        self.scores = [0] * number  # Initialize all scores to 0.

    def getName(self):
        """Returns the student's name."""
        return self.name

    def setScore(self, i, score):
        """Sets the ith score, counting from 1."""
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
        return f"Name: {self.name}\nScores: {' '.join(map(str, self.scores))}"

    def __eq__(self, other):
        """Tests for equality based on names."""
        return self.name == other.name

    def __lt__(self, other):
        """Tests if this student is less than another based on names."""
        return self.name < other.name

    def __ge__(self, other):
        """Tests if this student is greater than or equal to another based on names."""
        return self.name >= other.name


def main():
    """A simple test."""
    # Create two student objects
    student1 = Student("Jin", 3)
    student2 = Student("Jun", 3)

    # Print initial students
    print("Initial Students:")
    print(student1)
    print(student2)

    # Set scores for student1
    student1.setScore(1, 90)
    student1.setScore(2, 85)
    student1.setScore(3, 88)

    # Set scores for student2
    student2.setScore(1, 75)
    student2.setScore(2, 80)
    student2.setScore(3, 78)

    # Print updated students
    print("\nUpdated Students:")
    print(student1)
    print(student2)

    # Test comparison operators
    print("\nComparison Tests:")
    print(f"Is {student1.getName()} equal to {student2.getName()}? {student1 == student2}")
    print(f"Is {student1.getName()} less than {student2.getName()}? {student1 < student2}")
    print(f"Is {student1.getName()} greater than or equal to {student2.getName()}? {student1 >= student2}")


if __name__ == "__main__":
    main()
