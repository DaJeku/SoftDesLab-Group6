import sqlite3


conn = sqlite3.connect('adventure_tours.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS PARTICIPANT (
    p_number INTEGER PRIMARY KEY,
    last_name TEXT,
    first_name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    telephone_number TEXT,
    dob DATE
);
''')

# Create ADVENTURE_CLASS table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ADVENTURE_CLASS (
    class_number INTEGER PRIMARY KEY,
    class_description TEXT,
    max_people INTEGER,
    class_fee REAL
);
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS ENROLLMENT (
    p_number INTEGER,
    class_number INTEGER,
    class_date DATE,
    FOREIGN KEY(p_number) REFERENCES PARTICIPANT(p_number),
    FOREIGN KEY(class_number) REFERENCES ADVENTURE_CLASS(class_number),
    PRIMARY KEY (p_number, class_number, class_date)
);
''')


cursor.execute('''
INSERT INTO PARTICIPANT (p_number, last_name, first_name, address, city, state, postal_code, telephone_number, dob)
VALUES
(1, 'Doe', 'John', '123 Elm St', 'Springfield', 'IL', '62701', '555-1234', '1980-05-15'),
(2, 'Smith', 'Jane', '456 Oak St', 'Chicago', 'IL', '60601', '555-5678', '1990-08-22');
''')


cursor.execute('''
INSERT INTO ADVENTURE_CLASS (class_number, class_description, max_people, class_fee)
VALUES
(101, 'Hiking Basics', 20, 50.0),
(102, 'Advanced Biking', 15, 60.0);
''')

# Insert example data into ENROLLMENT table
cursor.execute('''
INSERT INTO ENROLLMENT (p_number, class_number, class_date)
VALUES
(1, 101, '2025-02-01'),
(2, 102, '2025-02-02');
''')

conn.commit()

print("Participant Details:")
cursor.execute('''
SELECT p_number, last_name, first_name, address, city, state, postal_code, telephone_number, dob
FROM PARTICIPANT;
''')
participants = cursor.fetchall()
for participant in participants:
    print(participant)


print("\nAdventure Class Details:")
cursor.execute('''
SELECT class_number, class_description, max_people, class_fee
FROM ADVENTURE_CLASS;
''')
classes = cursor.fetchall()
for class_info in classes:
    print(class_info)


print("\nEnrollment Details (for each participant enrolled in classes):")
cursor.execute('''
SELECT p.p_number, p.last_name, p.first_name, ac.class_number, ac.class_description, e.class_date
FROM ENROLLMENT AS e
JOIN PARTICIPANT AS p ON e.p_number = p.p_number
JOIN ADVENTURE_CLASS AS ac ON e.class_number = ac.class_number
ORDER BY p.p_number, ac.class_number, e.class_date;
''')
enrollments = cursor.fetchall()
for enrollment in enrollments:
    print(enrollment)


print("\nClass Participants (for each class):")
cursor.execute('''
SELECT e.class_date, ac.class_number, ac.class_description, p.p_number, p.last_name, p.first_name
FROM ENROLLMENT AS e
JOIN ADVENTURE_CLASS AS ac ON e.class_number = ac.class_number
JOIN PARTICIPANT AS p ON e.p_number = p.p_number
ORDER BY e.class_date, ac.class_number;
''')
class_participants = cursor.fetchall()
for class_participant in class_participants:
    print(class_participant)


conn.close()
