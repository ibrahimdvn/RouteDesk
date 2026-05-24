import sqlite3
import os
from datetime import datetime, timedelta
import random

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "RouteDesk.db")

class DBManager:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def init_db():
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        
        # Create Trips Table with realistic columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                company TEXT NOT NULL,
                route TEXT NOT NULL,
                departure TEXT NOT NULL,
                arrival TEXT NOT NULL,
                driver TEXT NOT NULL,
                plate TEXT NOT NULL,
                platform TEXT NOT NULL,
                price INTEGER NOT NULL,
                occupancy TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        
        try:
            cursor.execute("ALTER TABLE trips ADD COLUMN total_seats INTEGER DEFAULT 46")
            cursor.execute("ALTER TABLE trips ADD COLUMN layout TEXT DEFAULT '2+2'")
        except:
            pass
            
        # Create Bus Layouts Table for the interactive editor
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bus_layouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                data TEXT NOT NULL
            )
        """)
        
        # Create Operators Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL
            )
        """)
        
        # Create Customers Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                phone TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                tc_no TEXT NOT NULL
            )
        """)
        
        # Create Tickets Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_code TEXT NOT NULL,
                seat TEXT NOT NULL,
                passenger_name TEXT NOT NULL,
                tc_no TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        """)

        conn.close()

    @staticmethod
    def get_all_trips():
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trips ORDER BY departure ASC")
        trips = cursor.fetchall()
        conn.close()
        return trips

    @staticmethod
    def add_trip(code, company, route, departure, arrival, driver, plate, platform, price, occupancy, status, total_seats=46, layout="2+2"):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trips (code, company, route, departure, arrival, driver, plate, platform, price, occupancy, status, total_seats, layout) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (code, company, route, departure, arrival, driver, plate, platform, price, occupancy, status, total_seats, layout))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_trip(code):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trips WHERE code = ?", (code,))
        conn.commit()
        conn.close()

    @staticmethod
    def update_trip_status(code, new_status):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE trips SET status = ? WHERE code = ?", (new_status, code))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_customers():
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers ORDER BY name ASC")
        customers = cursor.fetchall()
        conn.close()
        return customers

    @staticmethod
    def add_customer(phone, name, tc_no):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO customers (phone, name, tc_no) 
            VALUES (?, ?, ?)
        """, (phone, name, tc_no))
        conn.commit()
        conn.close()

    @staticmethod
    def get_customer_by_phone(phone):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, tc_no FROM customers WHERE phone = ?", (phone,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def add_ticket(trip_code, seat, passenger_name, tc_no, price):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (trip_code, seat, passenger_name, tc_no, price) 
            VALUES (?, ?, ?, ?, ?)
        """, (trip_code, seat, passenger_name, tc_no, price))
        conn.commit()
        conn.close()

    @staticmethod
    def get_tickets_for_trip(trip_code):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT seat, passenger_name, tc_no, price FROM tickets WHERE trip_code = ?", (trip_code,))
        tickets = cursor.fetchall()
        conn.close()
        return tickets

    @staticmethod
    def delete_ticket(ticket_id):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def register_operator(username, password, full_name):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO operators (username, password, full_name) VALUES (?, ?, ?)", (username, password, full_name))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        conn.close()
        return success

    @staticmethod
    def verify_operator(username, password):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT full_name FROM operators WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        return None

    @staticmethod
    def save_bus_layout(name, data_json):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM bus_layouts WHERE name = ?", (name,))
        if cursor.fetchone():
            cursor.execute("UPDATE bus_layouts SET data = ? WHERE name = ?", (data_json, name))
        else:
            cursor.execute("INSERT INTO bus_layouts (name, data) VALUES (?, ?)", (name, data_json))
        conn.commit()
        conn.close()

    @staticmethod
    def get_bus_layouts():
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, data FROM bus_layouts")
        layouts = cursor.fetchall()
        conn.close()
        return layouts
