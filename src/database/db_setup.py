from sqlite3 import Error
from .db_connection import db_connection
#import models.system_admin
#import models.super_admin
#import models.consultant
#import models.member
import os

class db_setup:
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = db_connection(db_file)
        # self.delete_existing_db()
        self.create_tables()
        # self.seed_users()
        # self.seed_members()

    def delete_existing_db(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
            print("Existing database deleted")

    def create_tables(self):
        # used to create addresses & members tables
        sql_statements = [
            """CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY,
            street_name TEXT NOT NULL,
            house_num TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            city TEXT NOT NULL
            );""",
            """CREATE TABLE IF NOT EXISTS members (
                id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age TEXT NOT NULL,
                gender TEXT NOT NULL,
                weight REAL NOT NULL,
                address_id INT NOT NULL,
                email TEXT NOT NULL,
                mobile_phone TEXT NOT NULL,
                registration_date TEXT NOT NULL,
                FOREIGN KEY (address_id) REFERENCES addresses (id)
            );""",
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role INT NOT NULL CHECK (role IN ('0', '1', '2')),
                registration_date TEXT DEFAULT CURRENT_DATE
            );"""]

        db_conn = self.db.create_connection()
        cursor = db_conn.cursor()

        try:
            # create addresses and members tables
            for statement in sql_statements:
                cursor.execute(statement)
                # commit the changes
                db_conn.commit()
                print("Table created")
        except Error as e:
            print(e)
        finally:
            cursor.close()
            self.db.close_connection(db_conn)     
