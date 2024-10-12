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
        db = db_connection("um.db")

        conn = db.create_connection()
        cursor = conn.cursor()

        address_id = None

        # Check if the field is an address field since addresses & member info are two seperate tables
        if field_name in {"street_name", "house_num", "zip_code", "city"}:
            # Get the member details to retrieve address_id
            member = self.search_member(member_id)
            if member:
                address_id = member[0][6]  # Access the address_id from the first member entry
                query = f"UPDATE addresses SET {field_name} = ? WHERE id = ?"
            else:
                print(f"No member found with ID {member_id}")
                cursor.close()
                db.close_connection(conn)
                return
        else:
            # Safe parameterized query for updating members table
            query = f"UPDATE members SET {field_name} = ? WHERE id = ?"

        # Encrypt the new value
        if isinstance(new_value, (Gender, City)):
            new_value = database_encryption.encrypt_data(new_value.value)
        else:
            new_value = database_encryption.encrypt_data(new_value)

        if address_id:
            # Execute the UPDATE query for address
            cursor.execute(query, (new_value, address_id))
        else:
            # Execute the UPDATE query for member
            cursor.execute(query, (new_value, member_id))

        conn.commit()
        cursor.close()
        db.close_connection(conn)

        print(f"\nThe field {field_name} has been updated")


    def list_members(self):
        db = db_connection("src/um.db")

        conn = db.create_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, first_name, last_name, age, gender, weight, address_id, email, mobile_phone, registration_date FROM members")
        members = cursor.fetchall()
        if len(members) == 0:
            return False
        
        member_list = []
        for member in members:
            member_id, first_name, last_name, age, gender, weight, address_id, email, mobile_phone, registration_date = member
            
            first_name = database_encryption.decrypt_data(first_name)
            last_name = database_encryption.decrypt_data(last_name)
            age = database_encryption.decrypt_data(age)
            gender = database_encryption.decrypt_data(gender)
            weight = database_encryption.decrypt_data(weight)
            email = database_encryption.decrypt_data(email)
            mobile_phone = database_encryption.decrypt_data(mobile_phone)

            member_details = {
                "ID": member_id,
                "First Name": first_name,
                "Last Name": last_name,
                "Age": age,
                "Gender": gender,
                "Weight": weight,
                "Address ID": address_id,
                "Email": email,
                "Mobile Phone": mobile_phone,
                "Registration Date": registration_date
            }

            member_list.append(member_details)
        
        cursor.close()
        db.close_connection(conn)
        
        return member_list

    def search_member(self, search_key: str):
        db = db_connection("src/um.db")

        conn = db.create_connection()
        cursor = conn.cursor()
        
        member_list = self.list_members(self)
        address_list = self.list_addresses()

        search_key_lower = search_key.lower()

        search_results = []
        
        # check members & addresses tables
        for member in member_list:
            match_found = False # to track if search_key is found within this members info; once its found somewhere, the rest of the members info doesnt need to be checked since itll all be added to the result

            for key, value in member.items(): # loop through each key value pair in the dictionary
                if isinstance(value, str) and search_key_lower in value.lower(): # check if value contains search_key
                    search_results.append(member) # add all of the members info to search_results
                    match_found = True
                    break
            
            # if search_key isnt found in members table, check the linked address in the addresses table
            if not match_found:
                address = self.find_address(member['Address ID'])  # Get the member's address
                if address:
                    for key, value in address.items():
                        if isinstance(value, str) and search_key_lower in value:
                            match_found = True
                            break  # Stop checking address details if a match is found
            
            # if a match is found, add member info and their address info to the result
            if match_found:
                address = self.find_address(member['Address ID'])  # Get the member's address
                if address:
                    # Merge member and address dictionaries
                    member_with_address = {**member, **address}  # Combine member and address into one dictionary
                    search_results.append(member_with_address)

        cursor.close()
        db.close_connection(conn)

        return search_results

    def find_address(self, address_id):
        db = db_connection("src/um.db")

        conn = db.create_connection()
        cursor = conn.cursor()
        
        search_result_encrypted = cursor.execute("SELECT * FROM addresses WHERE id = ?", (address_id,)).fetchone()

        # check if search_result_encrypted isn't empty
        if search_result_encrypted:
            street_name = database_encryption.decrypt_data(search_result_encrypted[1])
            house_num = database_encryption.decrypt_data(search_result_encrypted[2])
            zip_code = database_encryption.decrypt_data(search_result_encrypted[3])
            city = database_encryption.decrypt_data(search_result_encrypted[4])

            address_details = {
                "ID": address_id,
                "Street Name": street_name,
                "House Number": house_num,
                "Zip Code": zip_code,
                "City": city
            }
        
            cursor.close()
            db.close_connection(conn)

            return address_details
        else:
            cursor.close()
            db.close_connection(conn)
            return None

    def list_addresses():
        db = db_connection("src/um.db")

        conn = db.create_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, street_name, house_num, zip_code, city FROM addresses")
        addresses = cursor.fetchall()
        if len(addresses) == 1 or len(addresses) == 0:
            return 
        
        address_list = []
        for address in addresses:
            address_id, street_name, house_num, zip_code, city = address

            street_name = database_encryption.decrypt_data(street_name)
            house_num = database_encryption.decrypt_data(house_num)
            zip_code = database_encryption.decrypt_data(zip_code)
            city = database_encryption.decrypt_data(city)

            address_details = {
                "ID": address_id,
                "Street Name": street_name,
                "House Number": house_num,
                "Zip Code": zip_code,
                "City": city
            }
        
        cursor.close()
        db.close_connection(conn)

        return address_list
    
    def search_member_id(self, member_id: str):
        db = db_connection("src/um.db")

        conn = db.create_connection()
        cursor = conn.cursor()
        
        search_result_encrypted = cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()

        # check if search_result_encrypted isn't empty
        if search_result_encrypted:
            first_name = database_encryption.decrypt_data(search_result_encrypted[1])
            last_name = database_encryption.decrypt_data(search_result_encrypted[2])
            age = database_encryption.decrypt_data(search_result_encrypted[3])
            gender = database_encryption.decrypt_data(search_result_encrypted[4])
            weight = database_encryption.decrypt_data(search_result_encrypted[5])
            email = database_encryption.decrypt_data(search_result_encrypted[7])
            mobile_phone = database_encryption.decrypt_data(search_result_encrypted[8])

            member_details = {
                "ID": member_id,
                "First Name": first_name,
                "Last Name": last_name,
                "Age": age,
                "Gender": gender,
                "Weight": weight,
                "Address ID": search_result_encrypted[6],
                "Email": email,
                "Mobile Phone": mobile_phone,
                "Registration Date": search_result_encrypted[9]
            }
        
            cursor.close()
            db.close_connection(conn)

            return member_details
        else:
            cursor.close()
            db.close_connection(conn)
            return None
