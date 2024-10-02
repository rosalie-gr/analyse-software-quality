from .consultant import Consultant
from .user import Role
from database.db_connection import db_connection
from etc.useractions.make_users import Make_users
from etc.useractions.update_users import Update_users
from etc.encryption.database_encryption import database_encryption

class SystemAdmin(Consultant):
    def __init__(self, first_name: str, last_name: str, username: str, password: str):
        super().__init__(first_name, last_name, username, password)
        self.role = Role.SYSTEM

    def list_users(self):
        db = db_connection("src/um.db")

        conn = db.create_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, first_name, last_name, username, role FROM users")
        users = cursor.fetchall()
        if len(users) == 1 or len(users) == 0:
            return False
        user_list = []
        for user in users:
            user_id, first_name, last_name, username, role = user
            if  username != 'super_admin':
                first_name = database_encryption.decrypt_data(first_name)
                last_name = database_encryption.decrypt_data(last_name)
                username = database_encryption.decrypt_data(username)
                role = role
                
                user_details = {
                    "ID": user_id,
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Username": username,
                    "Role": role
                }
                user_list.append(user_details)
        
        cursor.close()
        db.close_connection(conn)
        
        return user_list  

    def add_consultant(self):
        new_consultant = Make_users.make_Consultant()
        if new_consultant == False:
            print("Consultant not added, going back to main menu")
            return
        print(new_consultant[0], new_consultant[1], new_consultant[2], new_consultant[3])

        # now we need to add it to the database and encrypt
        db = db_connection("src/um.db")

        conn = db.create_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (first_name, last_name, username, password, role) VALUES (?, ?, ?, ?, ?)", 
                       (database_encryption.encrypt_data(new_consultant[0]),database_encryption.encrypt_data(new_consultant[1]), database_encryption.encrypt_data(new_consultant[2]), new_consultant[3], Role.CONSULT.value))
        conn.commit()
        print("Consultant added")

        cursor.close()
        db.close_connection(conn)

    def modify_consultant_info(self, consultant_id: str, field_name: str, new_value: str):
        #updated = Update_users.update_consultant(consultant_id, field_name, new_value)
        pass

    def delete_consultant(self, consultant_id):
        pass

    def reset_consultant_password(self, consultant_id):
        pass

    def search_user(self, user_id):
        pass

    def make_backup(self):
        # Add logic to make a backup of the system
        pass

    def restore_backup(self):
        # Add logic to restore the system from a backup
        pass

    def view_logs(self):
        pass

    def delete_member(self, member_id, address_id):
        pass
