from .system_admin import SystemAdmin
from .user import Role
from database.db_connection import db_connection
from etc.useractions.make_users import Make_users
from etc.useractions.update_users import Update_users
from etc.encryption.database_encryption import database_encryption

class SuperAdmin(SystemAdmin):
    def __init__(self):
        super().__init__("super", "admin", "super_admin", "Admin_123?")
        self.role = Role.SUPER

    def add_system_admin(self):
        new_sys_admin = Make_users.make_Sys_Admin()
        if new_sys_admin == False:
            print("System admin not added, going back to main menu")
            return
        # now we need to add it to the database and encrypt
        db = db_connection("src/um.db")
        conn = db.create_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (first_name, last_name, username, password, role) VALUES (?, ?, ?, ?, ?)", 
                       (database_encryption.encrypt_data(new_sys_admin.first_name),database_encryption.encrypt_data(new_sys_admin.last_name), database_encryption.encrypt_data(new_sys_admin.username), new_sys_admin.password, Role.CONSULT.value))
        conn.commit()
        print("Consultant added")

        cursor.close()
        db.close_connection(conn)


    def modify_system_admin_info(self, system_admin_id: str, field_name: str, new_value: str):
        pass

    def delete_system_admin(self, system_admin_id):
        pass

    def reset_system_admin_password(self, system_admin_id):
        pass