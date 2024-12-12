import sqlite3
from werkzeug.security import generate_password_hash

class UserDatabase:
    def __init__(self, db_name='users.db'):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            ''')

    def insert_user(self, username, password, role='public'):
        hashed_password = generate_password_hash(password)
        try:
            with self.connection:
                self.connection.execute('''
                    INSERT INTO users (username, password, role)
                    VALUES (?, ?, ?)
                ''', (username, hashed_password, role))
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists

    def close(self):
        self.connection.close()