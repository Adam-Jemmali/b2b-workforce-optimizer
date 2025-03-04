import sqlite3

conn = sqlite3.connect("workforce.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT,
    shift_start TEXT,
    shift_end TEXT,
    predicted_demand INTEGER
)
''')

conn.commit()
conn.close()

print("✅ Database setup complete!")
