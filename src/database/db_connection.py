import sqlite3
from sqlite3 import Error

class db_connection:
    # constructor method
    def __init__(self, db_file):
        self.db_file = db_file

    # create connection to sqlite database specified by db_file
    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(self.db_file)
            #print(f"Connected to {self.db_file}")
        except Error as e:
            print(e)
        return connection
    
    def close_connection(self, conn):
        if conn:
            conn.close()
            #print(f"Closed connection to {self.db_file}\n")
