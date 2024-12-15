import sqlite3

def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            place_of_birth TEXT NOT NUL
    ''')
    conn.commit()
    conn.close()

def add_user(username, email, date_of_birth, place_of_birth):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, email, date_of_birth, place_of_birth)
        VALUES (?, ?, ?, ?)
    ''', (username, email, date_of_birth, place_of_birth))
    conn.commit()
    conn.close()

create_table()
