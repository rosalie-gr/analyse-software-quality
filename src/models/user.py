from enum import Enum
from database.db_connection import db_connection
import etc.input_validations as v
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
    def change_password(self, new_password: str):
        if new_password == self.password:
            print("New password cannot be the same as the old password.")
            return False
        
        if v.validate_password(new_password):
            new_password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            
            # Update the password in the database
            db = db_connection("um.db")
            conn = db.create_connection()
            cursor = conn.cursor()

            try:
                query = "UPDATE users SET password = ? WHERE username = ?"
                cursor.execute(query, (new_password_hash, self.username))
                conn.commit()

                # If the database update is successful, update the instance variable
                self.password = new_password_hash
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
