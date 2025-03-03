import sqlite3
conn = sqlite3.connect('user_data.db')
# Create a cursor object
cursor = conn.cursor()
# Create a table to store user information
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    Last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE, 
    contact_number TEXT NOT NULL,
    password TEXT NOT NULL
)              
''')
# Commit the changes and close the connection
conn.commit()
conn.close ()