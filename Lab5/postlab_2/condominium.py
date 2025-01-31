import sqlite3

conn = sqlite3.connect('condo.db')
cursor = conn.cursor()

cursor.execute('PRAGMA foreign_keys = ON;')

def create_renter(conn, renter):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO renter (renter_number, first_name, middle_initial, last_name, address, city, state, postal_code, telephone_number, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', renter)
    conn.commit()

def get_renters(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM renter')
    return cursor.fetchall()

def update_renter(conn, renter):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE renter
        SET first_name = ?, middle_initial = ?, last_name = ?, address = ?, city = ?, state = ?, postal_code = ?, telephone_number = ?, email = ?
        WHERE renter_number = ?
    ''', renter[1:] + [renter[0]])
    conn.commit()

def delete_renter(conn, renter_number):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM renter WHERE renter_number = ?', (renter_number,))
    conn.commit()

def create_property(conn, property):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO property (condo_number, condo_name, address, city, state, postal_code, condo_unit, square_footage, number_of_rooms, number_of_bathrooms, maximum_pax, weekly_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', property)
    conn.commit()

def get_properties(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM property')
    return cursor.fetchall()

def update_property(conn, property):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE property
        SET condo_name = ?, address = ?, city = ?, state = ?, postal_code = ?, condo_unit = ?, square_footage = ?, number_of_rooms = ?, number_of_bathrooms = ?, maximum_pax = ?, weekly_rate = ?
        WHERE condo_number = ?
    ''', property[1:] + [property[0]])
    conn.commit()

def delete_property(conn, condo_number):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM property WHERE condo_number = ?', (condo_number,))
    conn.commit()

def create_rental_agreement(conn, rental_agreement):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO rental_agreement (rental_agreement_id, renter_number, condo_number, start_date, end_date, weekly_rental_amount)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', rental_agreement)
    conn.commit()

def get_rental_agreements(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rental_agreement')
    return cursor.fetchall()

def update_rental_agreement(conn, rental_agreement):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE rental_agreement
        SET renter_number = ?, condo_number = ?, start_date = ?, end_date = ?, weekly_rental_amount = ?
        WHERE rental_agreement_id = ?
    ''', rental_agreement[1:] + [rental_agreement[0]])
    conn.commit()

def delete_rental_agreement(conn, rental_agreement_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM rental_agreement WHERE rental_agreement_id = ?', (rental_agreement_id,))
    conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS renter (
    renter_number INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    middle_initial TEXT NOT NULL,
    last_name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    postal_code INT NOT NULL,
    telephone_number INT NOT NULL,
    email TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS property (
    condo_number INTEGER PRIMARY KEY,
    condo_name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    postal_code INT NOT NULL,
    condo_unit INT NOT NULL,
    square_footage INT NOT NULL,
    number_of_rooms INT NOT NULL,
    number_of_bathrooms INT NOT NULL,
    maximum_pax INT NOT NULL,
    weekly_rate INT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS rental_agreement (
    rental_agreement_id INTEGER PRIMARY KEY,
    renter_number INTEGER NOT NULL,
    condo_number INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    weekly_rental_amount REAL NOT NULL,
    FOREIGN KEY (renter_number) REFERENCES renter(renter_number),
    FOREIGN KEY (condo_number) REFERENCES property(condo_number)
)
''')

cursor.executemany('''
INSERT OR IGNORE INTO renter (renter_number, first_name, middle_initial, last_name, address, city, state, postal_code, telephone_number, email)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', [
    (1, 'Jane', 'A', 'Doe', '123 Elm St', 'Quezon City', 'NCR', 1101, 9123456789, 'jane.doe@example.com'),
    (2, 'John', 'B', 'Smith', '456 Pine Ave', 'Quezon City', 'NCR', 1102, 9876543210, 'john.smith@example.com'),
    (3, 'Alice', 'C', 'Brown', '789 Maple Blvd', 'Makati City', 'NCR', 1201, 9012345678, 'alice.brown@example.com')
])

cursor.executemany('''
INSERT OR IGNORE INTO property (condo_number, condo_name, address, city, state, postal_code, condo_unit, square_footage, number_of_rooms, number_of_bathrooms, maximum_pax, weekly_rate)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', [
    (1, 'Solmaris A', '111 Ocean Drive', 'Quezon City', 'NCR', 1101, 101, 1200, 3, 2, 6, 50000),
    (2, 'Solmaris B', '222 Beach Road', 'Quezon City', 'NCR', 1102, 102, 1500, 4, 3, 8, 65000),
    (3, 'Solmaris C', '333 Sun Avenue', 'Makati City', 'NCR', 1201, 103, 1800, 5, 4, 10, 80000)
])

cursor.executemany('''
INSERT OR IGNORE INTO rental_agreement (rental_agreement_id, renter_number, condo_number, start_date, end_date, weekly_rental_amount)
VALUES (?, ?, ?, ?, ?, ?)
''', [
    (1, 1, 1, '2025-02-01', '2025-02-08', 50000),
    (2, 2, 2, '2025-03-15', '2025-03-22', 65000),
    (3, 3, 3, '2025-04-10', '2025-04-17', 80000)
])



conn.commit()
conn.close()