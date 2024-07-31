from enum import Enum
from database.db_connection import db_connection
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
        pass

    # Checks the input password against the stored password
    def check_password(self, password: str):
        pass
