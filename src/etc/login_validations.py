from database.db_connection import db_connection
from etc.encryption.database_encryption import database_encryption
import bcrypt
from models.system_admin import SystemAdmin
from models.consultant import Consultant
import etc.validation_layer as v
from logger.logger import logger

def authenticate_user(username, password):
    db = db_connection("src/um.db")
    conn = db.create_connection()
    cursor = conn.cursor()

    if username == 'super_admin' and password == 'Admin_123?':

        logger.log_activity("super_admin", "Login", "Super Admin logged in")

        return cursor.execute("SELECT * FROM users WHERE id = ?", (1,)).fetchone()
    
    if username == 'super_admin' and password != 'Admin_123?':
        logger.log_activity(f"{username}", "Login", f"Failed login attempt for user {username}", username + password)
        return None

    # get decrypted list of users in DB
    user_list = SystemAdmin.list_users()

    # loop through list, looking for user with the right username
    user_id = None
    if user_list:
        for user in user_list :
            if user['Username'] == username:
                user_id = user['ID']
        if user_id == None:
            return None
    else:
        return None
    
    # select the user based on their ID in order to get their password
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_record = cursor.fetchone()

    if user_record:
        # Check if the password matches
        stored_password = user_record[4]
        
        if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
            logger.log_activity(f"{username}", "Login", f"User {username} logged in", username + password)
            return user_record
        
    cursor.close()
    conn.close()

    # Return None if authentication fails
    logger.log_activity(f"{username}", "Login", f"Failed login attempt for user {username}", username + password)
    return None

