from .user import User
from .user import Role
from .member import Member, Address, City, Gender
from database.db_connection import db_connection
from etc.useractions.make_users import Make_users
from etc.useractions.update_users import Update_users
from etc.encryption.database_encryption import database_encryption
from etc.member_helpers import member_helper

class Consultant(User):
    def __init__(self, first_name: str, last_name: str, username: str, password: str):
        super().__init__(first_name, last_name, username, password, Role.CONSULT)

    def add_member(self):
        new_member = Make_users.make_member()
        if not new_member:
            print("Member not added, returning to main menu.")
            return
        
        # Create new member and address objects
        new_address = Address(new_member[5], new_member[6], new_member[7], new_member[8])   
        member = Member(new_member[0], new_member[1], new_member[2], new_member[3], new_member[4], 
                        new_address, new_member[9], new_member[10])

        db = db_connection("src/um.db")
        conn = db.create_connection()
        cursor = conn.cursor()

        registration_date = member_helper.get_registration_date()
        Member.set_registration_date(member, registration_date)
        
        membership_id = member_helper.get_membership_id()
        Member.set_membership_id(member, membership_id)

        # Insert into address table
        cursor.execute("INSERT INTO addresses (street_name, house_num, zip_code, city) VALUES (?, ?, ?, ?)", 
                       (database_encryption.encrypt_data(member.address.street_name),
                        database_encryption.encrypt_data(member.address.house_number),
                        database_encryption.encrypt_data(member.address.zip_code),
                        database_encryption.encrypt_data(member.address.city.value)))
        conn.commit()

        # Get the ID of the last inserted address
        address_id = cursor.lastrowid

        # Insert into members table
        cursor.execute("""INSERT INTO members (id, first_name, last_name, age, gender, weight, address_id, email, 
                          mobile_phone, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (member.membership_id,
                        database_encryption.encrypt_data(member.first_name),
                        database_encryption.encrypt_data(member.last_name),
                        database_encryption.encrypt_data(member.age),
                        database_encryption.encrypt_data(member.gender.value),
                        database_encryption.encrypt_data(member.weight),
                        address_id,
                        database_encryption.encrypt_data(member.email),
                        database_encryption.encrypt_data(member.mobile_phone),
                        member.registration_date))
        conn.commit()

        print("Member added successfully.")
        cursor.close()
        db.close_connection(conn)

    def update_member(self, member_id: str, field_name: str, new_value: str):
        pass

    def display_members(self, members: list):
        pass
    
    def search_member(self, search_key: str):
        pass

    def find_address(self, address_id):
        pass