from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from Registration import register_user, login_user
from RideManagement import save_ride, search_rides  # Assuming this file exists

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session handling

# Create database if it doesn't exist
def create_database():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        contact_number TEXT NOT NULL,
        emailid TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS rides (
        ride_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ride_giver_id INTEGER NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        via TEXT,
        departure TIMESTAMP NOT NULL,
        available_seats INTEGER NOT NULL,
        FOREIGN KEY(ride_giver_id) REFERENCES users(id) ON DELETE CASCADE
    )''')
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def first_page():
    return render_template('first.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Capture form data and register user
        firstname = request.form.get("First Name")
        lastname = request.form.get("Last Name")
        contactno = request.form.get("Contact Number")
        emailid = request.form.get("emailid")
        password = request.form.get("password")
        cnfpassword = request.form.get("confirm-password")
        
        if password != cnfpassword:
            return render_template('signup.html', message="Passwords do not match.")
        
        create_database()
        try:
            register_user(firstname, lastname, contactno, emailid, password)
            return redirect(url_for('login_form'))
        except sqlite3.IntegrityError:
            return render_template('signup.html', message="Email already exists.")
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        email = request.form.get("emailid")
        password = request.form.get("password")
        login_result = login_user(email, password)

        if 'Welcome' in login_result:
            session['email'] = email  # Save user email in session
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message=login_result)
    
    return render_template('login.html')

@app.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('login_form'))
    
    return render_template('home.html')

@app.route('/offer', methods=['GET', 'POST'])
def offer_ride():
    if request.method == 'POST':
        from_place = request.form.get("from")
        to_place = request.form.get("to")
        via = request.form.get("via")
        seats = request.form.get("seats")
        date = request.form.get("date")
        time = request.form.get("time")

        # Save ride information to the database
        # Assuming ride_giver_id is obtained from the logged-in user
        ride_giver_id = 1  # Replace with actual user ID from session or database
        save_ride(ride_giver_id, from_place, to_place, via, seats, date, time)
        return render_template('offer.html', message="Ride offered successfully!")

    return render_template('offer.html')

@app.route('/find', methods=['GET', 'POST'])
def find_rides():
    if request.method == 'POST':
        from_place = request.form.get("from")
        to_place = request.form.get("to")
        find_date = request.form.get("date")
        find_time = request.form.get("time")

        # Query the database for available rides
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        # Assuming the format of 'find_date' and 'find_time' is 'YYYY-MM-DD' and 'HH:MM'
        query = '''
            SELECT * FROM rides
            WHERE origin = ? 
            AND destination = ? 
            AND departure LIKE ?
        '''
        departure_filter = f'{find_date} {find_time}%'

        cursor.execute(query, (from_place, to_place, departure_filter))
        rides = cursor.fetchall()
        conn.close()

        # If no rides are found, render a message, otherwise render the results
        if rides:
            return render_template('ride.html', rides=rides)
        else:
            return render_template('ride.html', message="No available rides found.")

    return render_template('find.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'email' not in session:
        return redirect(url_for('login_form'))
    
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Fetch user data
    cursor.execute('''SELECT first_name, last_name, contact_number, emailid FROM users WHERE emailid = ?''', (session['email'],))
    user = cursor.fetchone()

    if request.method == 'POST':
        # Get the updated data from the form
        updated_first_name = request.form['first_name']
        updated_last_name = request.form['last_name']
        updated_contact = request.form['contact_number']
        
        # Update user data in the database
        cursor.execute('''
            UPDATE users
            SET first_name = ?, last_name = ?, contact_number = ?
            WHERE emailid = ?
        ''', (updated_first_name, updated_last_name, updated_contact, session['email']))
        conn.commit()

        # After updating, reload the profile with updated data
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('email', None)  # Logout by clearing session
    return redirect(url_for('login_form'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
