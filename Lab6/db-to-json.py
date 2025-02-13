import sqlite3
import pandas as pd
import json

# Connect to the SQLite database
conn = sqlite3.connect("chinook.db")
cursor = conn.cursor()

# Get table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Export each table to JSON
for table in tables:
    table_name = table[0]
    df = pd.read_sql_query(f"SELECT * FROM test", conn)
    json_data = df.to_json(orient="records", indent=4)

    # Save JSON to a file
    with open(f"test.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_data)

    print(f"Exported test to test.json")

conn.close()