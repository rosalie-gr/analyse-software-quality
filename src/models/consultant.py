from .user import User
from .user import Role
from .member import Member, City, Gender
from database.db_connection import db_connection
from etc.useractions.make_users import Make_users
from .member import Member, Address

class Consultant(User):
    def __init__(self, first_name: str, last_name: str, username: str, password: str):
        super().__init__(first_name, last_name, username, password, Role.CONSULT)

    def add_member(self):
        # this makes a new member
        new_member = Make_users.make_member()
        if new_member == False:
            print("Member not added, going back to main menu")
            return
        newAdress = Address(new_member[5], new_member[6], new_member[7], new_member[8])   
        newmember = Member(new_member[0], new_member[1], new_member[2], new_member[3], new_member[4], newAdress, new_member[9], new_member[10])
        # now we need to add it to the database and encrypt that shit (rosalie task?? idk)

    def update_member(self, member_id: str, field_name: str, new_value: str):
        pass

    def display_members(self, members: list):
        pass
    
    def search_member(self, search_key: str):
        pass

    def find_address(self, address_id):
        pass