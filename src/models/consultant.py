from .user import User
from .user import Role
from .member import Member, City, Gender


class Consultant(User):
    def __init__(self, first_name: str, last_name: str, username: str, password: str):
        super().__init__(first_name, last_name, username, password, Role.CONSULT)

    def add_member(self, member: Member):
        pass

    def update_member(self, member_id: str, field_name: str, new_value: str):
        pass

    def display_members(self, members: list):
        pass
    
    def search_member(self, search_key: str):
        pass

    def find_address(self, address_id):
        pass