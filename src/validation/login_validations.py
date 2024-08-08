import bcrypt
import re
from database.db_connection import db_connection


def check_password(username):
    db = db_connection("um.db")
    conn = db.create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_record = cursor.fetchone()

    cursor.close()
    conn.close()

    # Return None if authentication fails
    return None


def authenticate_user(username, password):
    db = db_connection("um.db")
    conn = db.create_connection()
    cursor = conn.cursor()
    if username != 'super_admin':
        username = services.database_encryption.encrypt_data(username)

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_record = cursor.fetchone()
    cursor.close()
    conn.close()
    # Return None if authentication fails
    return None

