from .consultant import Consultant
from .user import Role
from database.db_connection import db_connection

class SystemAdmin(Consultant):
    def __init__(self, first_name: str, last_name: str, username: str, password: str):
        super().__init__(first_name, last_name, username, password)
        self.role = Role.SYSTEM

    def list_users(self):
        pass    

    def add_consultant(self, consultant_info):
        pass

    def modify_consultant_info(self, consultant_id: str, field_name: str, new_value: str):
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
