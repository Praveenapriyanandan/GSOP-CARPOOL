create schema gs;
create database gsop;
use gsop;
CREATE TABLE users (id INTEGER PRIMARY KEY,username VARCHAR(255) NOT NULL,role VARCHAR(50) NOT NULL,email VARCHAR(255) UNIQUE NOT NULL,password VARCHAR(255) NOT NULL);
INSERT INTO users (id, username, role, email, password) VALUES(1, 'Ashna', 'ride_giver', 'ashna@gmail.com', 'ashna123');
INSERT INTO users (id, username, role, email, password) VALUES(2, 'Praveena', 'passenger', 'praveena@gmail.com ', 'praveena456');
INSERT INTO users (id, username, role, email, password) VALUES(3, 'Midhuna', 'ride_giver', 'midhuna@gmail.com', 'midhuna789');
INSERT INTO users (id, username, role, email, password) VALUES(4, 'Thansi', 'passenger', 'thansi@gmail.com', 'thansi123');
INSERT INTO users (id, username, role, email, password) VALUES(5, 'Janaki', 'ride_giver', 'janaki@gmail.com', 'janaki123');
INSERT INTO users (id, username, role, email, password) VALUES(6, 'Chandana', 'passenger', 'chandana@gmail.com', 'chandana123');
INSERT INTO users (id, username, role, email, password) VALUES(7, 'Kevin', 'ride_giver', 'kevin@gmail.com', 'kevin123');
INSERT INTO users (id, username, role, email, password) VALUES(8, 'Adhith', 'passenger', 'adhith@gmail.com', 'adhith321');
INSERT INTO users (id, username, role, email, password) VALUES(9, 'Aswin', 'ride_giver', 'aswin@gmail.com', 'aswin321');
delete from users where id='101';



select * from users;
CREATE TABLE ride (ride_id INTEGER PRIMARY KEY,ride_giver_id INTEGER NOT NULL,origin VARCHAR(255) NOT NULL,destination VARCHAR(255) NOT NULL,departure TIMESTAMP NOT NULL,available_seats INTEGER NOT NULL CHECK (available_seats >= 0),FOREIGN KEY (ride_giver_id) REFERENCES users(id) ON DELETE CASCADE);
INSERT INTO ride (ride_id, ride_giver_id, origin, destination, departure, available_seats) VALUES
(1, 1, 'Kochi', 'Thiruvananthapuram', '2025-03-01 08:30:00', 3),
(2, 3, 'Kozhikode', 'Kannur', '2025-03-03 07:45:00', 4),
(3, 5, 'Thrissur', 'Palakkad', '2025-03-05 09:00:00', 5),
(4, 7, 'Alappuzha', 'Kottayam', '2025-03-07 14:45:00', 2)
(5, 1, 'Kozhikode', 'Kasargod', '2025-03-07 14:45:00', 5);
INSERT INTO ride (ride_id, ride_giver_id, origin, destination, departure, available_seats) VALUES

(6, 3, 'Wayanad', 'Idukki', '2025-03-07 14:45:00', 7),
(7, 5, 'Palakkad', 'Kottayam', '2025-03-07 14:45:00', 2),
(8, 1, 'Alappuzha', 'Thiruvananthapuram', '2025-03-07 14:45:00', 4),
(9, 3, 'Malappuram', 'Eranakulam', '2025-03-07 14:45:00', 5),
(10, 9, 'Ernakulam', 'Kollam', '2025-03-09 06:30:00', 3);


select * from ride;


CREATE TABLE Booking (booking_id INTEGER PRIMARY KEY,ride_id INTEGER NOT NULL,passenger_id INTEGER NOT NULL,booking_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,status VARCHAR(50) NOT NULL CHECK (status IN ('Confirmed', 'Cancelled', 'Pending')),FOREIGN KEY (ride_id) REFERENCES ride(ride_id) ON DELETE CASCADE,FOREIGN KEY (passenger_id) REFERENCES users(id) ON DELETE CASCADE);
INSERT INTO Booking (booking_id, ride_id, passenger_id, booking_datetime, status) VALUES
(301, 1, 2, '2025-02-20 10:00:00', 'Confirmed'),  
(302, 2, 4, '2025-02-21 11:30:00', 'Pending'),  
(303, 3, 6, '2025-02-22 12:45:00', 'Confirmed'),  
(304, 4, 8, '2025-02-23 14:00:00', 'Cancelled'),  
(305, 5, 2, '2025-02-24 15:15:00', 'Confirmed');  

select * from Booking;
CREATE TABLE Payment (payment_id INTEGER PRIMARY KEY,booking_id INTEGER NOT NULL,amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0),payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY (booking_id) REFERENCES Booking(booking_id) ON DELETE CASCADE);

INSERT INTO Payment (payment_id, booking_id, amount, payment_date) VALUES
(401, 301, 25.00, '2025-02-20 10:30:00'),  
(402, 303, 30.50, '2025-02-22 13:00:00'),  
(403, 305, 20.00, '2025-02-24 15:45:00'),  
(404, 302, 15.75, '2025-02-21 11:35:00');  

SELECT * FROM Payment;
select username from users;

select  * from ride where ride_giver_id='3';

select u.username from booking b join users u on b.passenger_id = u.id where b.ride_id = '1';  

select * from ride where ride_giver_id = '1' or ride_id in (select ride_id from booking where passenger_id = '4');  

select * from ride where origin = 'Alappuzha' and destination = 'Thiruvananthapuram';  

select ride_id, count(passenger_id) as passenger_count from booking group by ride_id;  

select * from ride where departure ='2025-03-07 14:45:00';  

select distinct u.username from users u join ride r on u.id = r.ride_giver_id where r.departure = '2025-03-07 14:45:00';  

select * from ride where origin = 'Alappuzha' and available_seats > 2;
  
select u.username, count(r.ride_id) as total_rides from users u join ride r on u.id = r.ride_giver_id group by u.username having count(r.ride_id) > 1;  

select * from ride where origin = 'Alappuzha'and departure = '2025-03-07 14:45:00' and available_seats > 0;
  
select * from ride where origin = 'Alappuzha'or destination = 'Kottayam';  

select * from ride order by departure desc limit 1; 
 
select origin, destination, count(*) as frequency from ride group by origin, destination order by frequency desc; 
 
select * from ride where time(departure) between '08:00:00' and '15:00:00';


