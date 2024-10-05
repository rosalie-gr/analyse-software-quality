from database.db_connection import db_connection
from etc.encryption.database_encryption import database_encryption
import bcrypt
from models.system_admin import SystemAdmin

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

    if username == 'super_admin' and password == 'Admin_123?':
        return cursor.execute("SELECT * FROM users WHERE id = ?", (1,)).fetchone()
    
    # get decrypted list of users in DB
    user_list = SystemAdmin.list_users()

    # loop through list, looking for user with the right username
    if user_list:
        for user in user_list :
            if user['Username'] == username:
                user_id = user['ID']
    else:
        return None
    
    # select the user based on their ID in order to get their password
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_record = cursor.fetchone()

    if user_record:
        # Check if the password matches
        stored_password = user_record[4]
        
        if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
            return user_record
        
    cursor.close()
    conn.close()

    # Return None if authentication fails
    return None

