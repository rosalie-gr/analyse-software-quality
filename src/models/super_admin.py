from .system_admin import SystemAdmin
from .user import Role
from database.db_connection import db_connection

class SuperAdmin(SystemAdmin):
    def __init__(self):
        super().__init__("super", "admin", "super_admin", "Admin_123?")
        self.role = Role.SUPER

    def add_system_admin(self, system_admin_info):
        pass

    def modify_system_admin_info(self, system_admin_id: str, field_name: str, new_value: str):
        pass

    def delete_system_admin(self, system_admin_id):
        pass

    def reset_system_admin_password(self, system_admin_id):
        pass