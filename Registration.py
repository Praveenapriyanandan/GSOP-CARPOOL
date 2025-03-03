import sqlite3
import re
# Function to register a new user
def register_user(first_name, last_name, email, contact_number, password):   
   conn = sqlite3.connect('user_data.db')    
   cursor = conn.cursor()  
      # Basic validation for email and contact number   
   if not re.match(r"[^@]+@[^@]+\.[^@]+", email):       
      return "Invalid email address"   
   if not re.match(r"^\d{10}$", contact_number):     
      return "Invalid contact number. It should be 10 digits."  
   try:     
      # Insert user data into the database    
      cursor.execute('''    
      INSERT INTO users (first_name, last_name, email, contact_number, password)    
      VALUES (?, ?, ?, ?, ?)     
      ''', (first_name, last_name, email, contact_number, password))   
      conn.commit()    
      return "User registered successfully"  
   except sqlite3.IntegrityError:    
      return "Error: Email already registered"   
   finally:      
      conn.close()