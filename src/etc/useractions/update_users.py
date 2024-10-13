import re
import bcrypt
from etc import validation_layer as v
from models.member import Gender, City, Member  

class Update_users:
    def update_member(member: Member):
        print("Select the field to edit:")
        fields = {
            "1": ("first_name", v.name_check, member.first_name),
            "2": ("last_name", v.name_check, member.last_name),
            "3": ("age", v.number_check, member.age),
            "4": ("gender", Gender, member.gender),  # Assuming Gender is an enum
            "5": ("weight", v.number_check, member.weight),
            "6": ("street_name", v.name_check, member.address.street_name),
            "7": ("house_num", v.number_check, member.address.house_number),
            "8": ("zip_code", v.zip_code_check, member.address.zip_code),
            "9": ("city", City, member.address.city),  # Assuming City is an enum
            "10": ("email", v.email_check, member.email),
            "11": ("mobile_phone", v.phone_check, member.mobile_phone),
        }
        
        for key, (field_name, _, current_value) in fields.items():
            print(f"{key}: {field_name} (current: {current_value})")
        
        print("\n")

        field_choice = input("Enter the number of the field you want to edit: ")

        if field_choice not in fields:
            print("Invalid choice.")
            return None

        field_name, validation_func, _ = fields[field_choice]
        
        if field_choice in ["4", "9"]:  # Enum fields
            new_value = v.get_enum_input(validation_func, f"Enter new {field_name}: ", False )
        else:
            new_value = v.get_valid_input(validation_func, f"Enter new {field_name}: ", False)
        
        if new_value:
            return field_name, new_value
        else:
            print(f"No new value was given.")
            return None

    def update_consultant(consultant):
        if consultant.role != 0:
            print("This user is not a consultant.")
            return None
        print("Select the field to edit:")
        fields = {
            "1": ("first_name", v.name_check, consultant.first_name),
            "2": ("last_name", v.name_check, consultant.last_name),
            "3": ("username", v.validate_username, consultant.username),
            "4": ("password", v.validate_password,  '********')  # Mask password
        }
        
        for key, (field_name, _, current_value) in fields.items():
            print(f"{key}: {field_name} (current: {current_value})")

        field_choice = input("Enter the number of the field you want to edit: ")

        if field_choice not in fields:
            return None

        field_name, validation_func, _ = fields[field_choice]

        if field_name == "password":
            new_value = v.prompt_password(f"Enter new {field_name}: ", validation_func, 3)
        else:
            new_value = v.get_valid_input(validation_func, f"Enter new {field_name}: ", False)
        
        if new_value:
            return field_name, new_value
        else:
            print(f"No new value was given.")
            return None


    def update_system_admin(system_admin):
        if system_admin.role != 1:
            print("This user is not a system admin.")
            return None
        print("Select the field to edit:")
        fields = {
            "1": ("first_name", v.name_check, system_admin.first_name),
            "2": ("last_name", v.name_check, system_admin.last_name),
            "3": ("username", v.validate_username, system_admin.username),
            "4": ("password", v.validate_password, '********')  # Mask password
        }
        
        for key, (field_name, _, current_value) in fields.items():
            print(f"{key}: {field_name} (current: {current_value})")

        field_choice = input("Enter the number of the field you want to edit: ")

        if field_choice not in fields:
            return None

        field_name, validation_func, _ = fields[field_choice]

        if field_name == "password":
            new_value = v.prompt_password(f"Enter new {field_name}: ", validation_func, 3)
        else:
            new_value = v.get_valid_input(validation_func, f"Enter new {field_name}: ", False)
        
        if new_value:
            if field_choice == "4":  # Password needs to be hashed
                new_value = bcrypt.hashpw(new_value.encode(), bcrypt.gensalt()).decode()
            return field_name, new_value
        else:
            print(f"No new value was given.")
            return None
