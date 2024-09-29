from database.db_connection import db_connection
from etc.encryption.database_encryption import database_encryption
import bcrypt



def check_password(username):
    db = db_connection("src/um.db")
    conn = db.create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_record = cursor.fetchone()

    cursor.close()
    conn.close()

    # Return None if authentication fails
    return None


def authenticate_user(username, password):
    db = db_connection("src/um.db")
    conn = db.create_connection()
    cursor = conn.cursor()
    if username != 'super_admin':
        username = database_encryption.encrypt_data(username)

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_record = cursor.fetchone()
    if user_record:
        # Check if the password matches
        stored_password = user_record[4]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return user_record
    cursor.close()
    conn.close()
    # Return None if authentication fails
    return None

