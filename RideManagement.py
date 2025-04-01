import sqlite3

def save_ride(ride_giver_id, from_place, to_place, via, seats, date, time):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO rides (ride_giver_id, origin, destination, via, departure, available_seats)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (ride_giver_id, from_place, to_place, via, f'{date} {time}', seats))
    conn.commit()
    conn.close()

def search_rides(from_place, to_place, find_date, find_time):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM rides
    WHERE origin = ? AND destination = ? AND departure >= ? AND departure <= ?
    ''', (from_place, to_place, f'{find_date} {find_time}', f'{find_date} {find_time}'))
    rides = cursor.fetchall()
    conn.close()
    return rides
