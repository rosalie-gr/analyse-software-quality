import re
import etc.validation_layer as v
from models.member import Gender, City  
from models.user import User

# Functions to create new users and members
class Make_users:
    def make_member():
        print("Enter member details:")
        first_name = v.get_valid_input(v.name_check, "First name: ", False, True)
        if not first_name: return False

        last_name = v.get_valid_input(v.name_check, "Last name: ", False, True)
        if not last_name: return False

        age = v.get_valid_input(v.number_check, "Age: ", False, True)
        if not age: return False
        age = int(age)

        gender = v.get_enum_input("Gender: ",Gender, 3)
        if not gender: return False

        weight = v.get_valid_input(v.number_check, "Weight: ", False, True)
        if not weight: return False

        street_name = v.get_valid_input(v.name_check, "Street name: ", False, True)
        if not street_name: return False

        house_number = v.get_valid_input(v.number_check, "House number: ", False, True)
        if not house_number: return False

        zip_code = v.get_valid_input(v.zip_code_check, "Zip code: ", False, True)
        if not zip_code: return False

        city = v.get_enum_input("City: ",City, 3)
        if not city: return False

        email = v.get_valid_input(v.email_check, "Email: ", False, True)
        if not email: return False

        mobile_phone = v.get_valid_input(v.phone_check, "Mobile phone: ", False, True)
        if not mobile_phone: return False
        
        return first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email, mobile_phone

    def make_Consultant():
        print("Enter Consultant details")
        first_name = v.get_valid_input(v.name_check, "First name: ", False, True)
        if not first_name: return False

        last_name = v.get_valid_input(v.name_check, "Last name: ", False, True)
        if not last_name: return False

        username = v.get_valid_input(v.validate_username, "Username: ", False, True)
        if not username: return False
        unique = User.check_username(username)
        if not unique:
            return False

        password = v.get_valid_input(v.validate_password, "Password: ", False, True)
        if not password: return False

        cons = User(first_name, last_name, username, password, 0)
        return cons

    def make_Sys_Admin():
        print("Enter system admin details")
        first_name = v.get_valid_input(v.name_check, "First name: ", False, True)
        if not first_name: return False

        last_name = v.get_valid_input(v.name_check, "Last name: ", False, True)
        if not last_name: return False

        username = v.get_valid_input(v.validate_username, "Username: ", False, True)
        if not username: return False
        unique = User.check_username(username)
        if not unique:
            return False

        password = v.get_valid_input(v.validate_password, "Password: ", False, True)
        if not password: return False

        sys = User(first_name, last_name, username, password, 1)
        return sys
