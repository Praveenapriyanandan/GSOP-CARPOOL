import sqlite3

def login_user(email, password):  
    conn = sqlite3.connect('user_data.db')   
    cursor = conn.cursor()   
    cursor.execute('''   
    SELECT * FROM users WHERE emailid = ? AND password = ?   
    ''', (email, password))  
    user = cursor.fetchone()  
    conn.close()   
    if user:       
        return f"Welcome {user[1]} {user[2]}!"  # Returning the full name of the user
    else:     
        return "Login failed: Invalid email or password"
