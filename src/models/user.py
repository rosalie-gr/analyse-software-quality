from enum import Enum
from database.db_connection import db_connection
from etc.encryption.database_encryption import database_encryption
import etc.validation_layer as v
import bcrypt

class Role(Enum):
    SUPER = 2
    SYSTEM = 1
    CONSULT = 0


class User:
    def __init__(self, first_name: str, last_name: str, username: str, password: str, role: Role):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.role = role

    # Changes the password of the user
    def change_password(self):
        new_password = input("Enter new password: ")
          
        if new_password == self[4]:
            print("New password cannot be the same as the old password.")
            return False
        
        if v.validate_password(new_password):
            new_password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            username = self[3]
            id = self[0]
            print(f"Changing password for user: {username} with ID: {id}")
            
            # Update the password in the database
            db = db_connection("src/um.db")
            conn = db.create_connection()
            cursor = conn.cursor()

            try:
                query = "UPDATE users SET password = ? WHERE id = ?"
                cursor.execute(query, (new_password_hash, id))
                conn.commit()

                if cursor.rowcount == 1:
                    print("Password update query executed successfully.")
                else:
                    print("Password update failed: No rows were affected.")
                    return False
        
                print("\nPassword changed successfully.")
                return True
            except Exception as e:
                print(f"An error occurred while updating the password: {e}")
                return False
            finally:
                cursor.close()
                db.close_connection(conn)
        else:
            return False

    # Checks the input password against the stored password
    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password.encode())

    def search_user(self, user_id):
        db = db_connection("src/um.db")

        conn = db.create_connection()
        cursor = conn.cursor()

        if (user_id.isnumeric()):
            result = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

        if (result):
            decrypt_user = {
                "ID": result[0],
                "first_name": database_encryption.decrypt_data(result[1]),
                "last_name": database_encryption.decrypt_data(result[2]),
                "username": database_encryption.decrypt_data(result[3]),
                "password": result[4],
                "role": result[5]
            }
            user = User(decrypt_user["first_name"], decrypt_user["last_name"], decrypt_user["username"], decrypt_user["password"], decrypt_user["role"])
            return user
        else:
            print("User not found")
            return False
    
    def check_username(username: str):
        db = db_connection("src/um.db")
        conn = db.create_connection()
        cursor = conn.cursor()
        
        query = "SELECT username FROM users"
        result = cursor.execute(query)
        result = result.fetchall()
        for row in result:
            if row[0] != 'super_admin':
                if database_encryption.decrypt_data(row[0]) == username:
                    print("Username already exists.")
                    return False
        return True