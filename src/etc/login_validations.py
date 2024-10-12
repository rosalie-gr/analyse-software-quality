from database.db_connection import db_connection
from etc.encryption.database_encryption import database_encryption
import bcrypt
from models.system_admin import SystemAdmin
from models.consultant import Consultant
import etc.validation_layer as v

# def check_if_temp_pass(username):
#     db = db_connection("src/um.db")
#     conn = db.create_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
#     user_record = cursor.fetchone()

#     if user_record:
#         db_password_hash = user_record[4]  

#         temp_password = "Temp_password!"
#         if bcrypt.checkpw(temp_password.encode(), db_password_hash.encode()): 
#             print("Your password has been reset. Please change your password.")
#             new_password = input("Enter new password: ")
#             is_valid = v.validate_password(new_password)
#             if not is_valid:
#                 print("Invalid password.")
#                 return None
#             consult = Consultant(user_record[1], user_record[2], user_record[3], new_password)
#             Consultant.change_password(consult, new_password)
#             print("Log in again with your new password.")
#             return True
#     else:
#         # User not found in the database
#         return False

#     cursor.close()
#     conn.close()

#     # Return None if authentication fails
#     return None


def authenticate_user(username, password):
    db = db_connection("src/um.db")
    conn = db.create_connection()
    cursor = conn.cursor()

    if username == 'super_admin' and password == 'Admin_123?':
        return cursor.execute("SELECT * FROM users WHERE id = ?", (1,)).fetchone()
    
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
            return user_record
        
    cursor.close()
    conn.close()

    # Return None if authentication fails
    return None

