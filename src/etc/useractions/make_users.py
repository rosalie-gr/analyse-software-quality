import re
import etc.validation_layer as v
from models.member import Gender, City  
from models.user import User

# Functions to create new users and members
class Make_users:
    def make_member():
        print("Enter member details:")
        first_name = v.get_valid_input("First name: ", v.name_check)
        if not first_name: return False

        last_name = v.get_valid_input("Last name: ", v.name_check)
        if not last_name: return False

        age = v.get_valid_input("Age: ", v.number_check)
        if not age: return False
        age = int(age)

        gender = v.get_enum_input("Gender:", Gender)
        if not gender: return False

        weight = v.get_valid_input("Weight: ", v.number_check)
        if not weight: return False

        street_name = v.get_valid_input("Street name: ", v.name_check)
        if not street_name: return False

        house_number = v.get_valid_input("House number: ", v.number_check)
        if not house_number: return False

        zip_code = v.get_valid_input("Zip code: ", v.zip_code_check)
        if not zip_code: return False

        city = v.get_enum_input("City: ", City)
        if not city: return False

        email = v.get_valid_input("Email: ", v.email_check)
        if not email: return False

        mobile_phone = v.get_valid_input("Mobile phone: ", v.phone_check)
        if not mobile_phone: return False
        
        return first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email, mobile_phone

    def make_Consultant():
        print("Enter Consultant details")
        first_name = v.get_valid_input("First name: ", v.name_check)
        if not first_name: return False

        last_name = v.get_valid_input("Last name: ", v.name_check)
        if not last_name: return False

        username = v.get_valid_input("Username: ", v.validate_username)
        if not username: return False

        password = v.get_valid_input("Password: ", v.validate_password)
        if not password: return False

        cons = User(first_name, last_name, username, password, 0)
        return cons

    def make_Sys_Admin():
        print("Enter system admin details")
        first_name = v.get_valid_input("First name: ", v.name_check)
        if not first_name: return False

        last_name = v.get_valid_input("Last name: ", v.name_check)
        if not last_name: return False

        username = v.get_valid_input("Username: ", v.validate_username)
        if not username: return False

        password = v.get_valid_input("Password: ", v.validate_password)
        if not password: return False

        sys = User(first_name, last_name, username, password, 1)
        return sys
