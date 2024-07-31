import re
from models.member import Gender, City, Member, Address
from database.db_connection import db_connection
import bcrypt
import getpass
from services.encryption import encrypt_master_aes_key, decrypt_master_aes_key


# general function to get valid input from the user
def get_valid_input(prompt, validation_func):
    attempts = 0
    while attempts < 3:
        value = input(prompt)
        if length_check(value) == False:
            attempts += 1
            print(f"Attempt {attempts}/3 failed. Try again.")
            continue
        if validation_func(value):
            return value
        attempts += 1
        print(f"Attempt {attempts}/3 failed. Try again.")
    print("\nToo many failed attempts.")
    return False

def length_check(value):
    if len(value) < 30:
        print(f"Input is too long! Maximum allowed length is 30.")
        return True
    return False

def get_valid_sup_password(prompt):
    attempts = 0
    while attempts < 3:
        password = getpass.getpass(prompt)
        if password == 'Admin_123?':
            return password
        else:
            # not true for sup_admin, but this way they won't know that I guess?
            print("Password must be at least 12 characters long and no longer than 30 characters, and contain at least one lowercase letter, one uppercase letter, one digit, and one special character (~!@#$%&_-+=`|\\(){}[]:;'<>,.?/).")
            attempts += 1
            print(f"Attempt {attempts}/3 failed. Try again.")
    print("\nToo many failed attempts.")
    return False

def prompt_password(prompt, validation_func):
    attempts = 0
    while attempts < 3:
        password = getpass.getpass(prompt)
        if validation_func(password):
            return password
        print(f"Attempt {attempts}/3 failed. Try again.")
    print("\nToo many failed attempts.")
    return False

# specific validation functions
def name_check(word):
    # check if word is empty or contains only letters, spaces, hyphens, apostrophes, and accents
    if word and re.match(r"^[a-zA-Z\s\-\'\u00C0-\u017F]*$", word):
        return True
    print("Input must contain only letters, spaces, hyphens, apostrophes, and accents.")
    return False

def number_check(number):
    if re.match(r'^[0-9]*$', number):
        return True
    print("Input must be a number.")
    return False

def zip_code_check(zip_code):
    if not re.match(r'^[0-9]{4}[a-zA-Z]{2}$', zip_code):
        return True
    print("Zip code must be exactly 6 digits with 2 letters at the end.")
    return False

def email_check(email):
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return True
    print("Invalid email format.")
    return False

def phone_check(phone):
    if re.match(r'^\+?[0-9\s\-]{7,15}$', phone):
       return True
    print("Phone number must be between 7 and 15 digits, and can include spaces, dashes, and an optional leading '+'.")
    return False

def validate_username(username):
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_.\']{7,9}$', username):
        return True
    print("Username must have a length of 8-10 characters, start with a letter or underscore (_), and contain only letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (.).")
    return False

def validate_password(password):
    if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-\+=`|\\(){}[\]:;\'<>,.?/])[A-Za-z\d~!@#$%&_\-\+=`|\\(){}[\]:;\'<>,.?/]{12,30}$', password):
        return True
    print("Password must be at least 12 characters long and no longer than 30 characters, and contain at least one lowercase letter, one uppercase letter, one digit, and one special character (~!@#$%&_-+=`|\\(){}[]:;'<>,.?/).")
    return False

def search_key_check(search_key):
    if re.match(r'^[a-zA-Z0-9\s\-\'\u00C0-\u017F]*$', search_key):
        return True
    print("Search key must only contain letters (a-z), numbers (0-9), spaces, hyphens, apostrophes, and accents.")
    return False

# Enum input function
def get_enum_input(prompt, enum):
    attempts = 0
    while attempts < 3:
        print(prompt)
        for item in enum:
            print(f"{item.name}: {item.value}")
        value = input("Select from the above options (input from the first collum): ").upper()
        if value in enum.__members__ or value in enum.__members__.values():
            return enum[value]
        attempts += 1
        print(f"Attempt {attempts}/3 failed. Try again.")
    print("Too many failed attempts.")
    return None

# Functions to create new users and members
def make_member():
    print("Enter member details:")
    first_name = get_valid_input("First name: ", name_check)
    if not first_name: return False

    last_name = get_valid_input("Last name: ", name_check)
    if not last_name: return False

    age = get_valid_input("Age: ", number_check)
    if not age: return False
    age = int(age)

    gender = get_enum_input("Gender:", Gender)
    if not gender: return False

    weight = get_valid_input("Weight: ", number_check)
    if not weight: return False

    street_name = get_valid_input("Street name: ", name_check)
    if not street_name: return False

    house_number = get_valid_input("House number: ", number_check)
    if not house_number: return False

    zip_code = get_valid_input("Zip code: ", zip_code_check)
    if not zip_code: return False

    city = get_enum_input("City: ", City)
    if not city: return False

    email = get_valid_input("Email: ", email_check)
    if not email: return False

    mobile_phone = get_valid_input("Mobile phone: ", phone_check)
    if not mobile_phone: return False
    return first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email, mobile_phone

def make_Consultant():
    print("Enter Consultant details")
    first_name = get_valid_input("First name: ", name_check)
    if not first_name: return False

    last_name = get_valid_input("Last name: ", name_check)
    if not last_name: return False

    username = get_valid_input("Username: ", validate_username)
    if not username: return False

    password = get_valid_input("Password: ", validate_password)
    if not password: return False

    return first_name, last_name, username, password

def make_Sys_Admin():
    print("Enter system admin details")
    first_name = get_valid_input("First name: ", name_check)
    if not first_name: return False

    last_name = get_valid_input("Last name: ", name_check)
    if not last_name: return False

    username = get_valid_input("Username: ", validate_username)
    if not username: return False

    password = get_valid_input("Password: ", validate_password)
    if not password: return False

    return first_name, last_name, username, password

# Function to update user/member details
def update_member(member: Member):
    
    print("Select the field to edit:")
    fields = {
        "1": ("first_name", name_check, member.first_name),
        "2": ("last_name", name_check, member.last_name),
        "3": ("age", number_check, member.age),
        "4": ("gender", Gender, member.gender),
        "5": ("weight", number_check, member.weight),
        "6": ("street_name", name_check, member.address.street_name),
        "7": ("house_num", number_check, member.address.house_number),
        "8": ("zip_code", zip_code_check, member.address.zip_code),
        "9": ("city", City, member.address.city),
        "10": ("email", email_check, member.email),
        "11": ("mobile_phone", phone_check, member.mobile_phone),
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
        new_value = get_enum_input(f"Enter new {field_name}: ", validation_func)
    else:
        new_value = get_valid_input(f"Enter new {field_name}: ", validation_func)
    if new_value:
        return field_name, new_value
    else:
        print(f"No new value was given.")
        return None

def update_consultant(consultant):
    print("Select the field to edit:")
    fields = {
        "1": ("first_name", name_check, consultant.first_name),
        "2": ("last_name", name_check, consultant.last_name),
        "3": ("username", validate_username, consultant.username),
        "4": ("password", validate_password,  '********')  # Mask password
    }
    
    for key, (field_name, _, current_value) in fields.items():
        print(f"{key}: {field_name} (current: {current_value})")

    field_choice = input("Enter the number of the field you want to edit: ")

    if field_choice not in fields:
        return None

    field_name, validation_func, _ = fields[field_choice]

    if field_name == "password":
        new_value = prompt_password(f"Enter new {field_name}: ", validation_func)
    else:
        new_value = get_valid_input(f"Enter new {field_name}: ", validation_func)
    
    if new_value:
        return field_name, new_value
    else:
        print(f"No new value was given.")
        return None


def update_system_admin(system_admin):
    print("Select the field to edit:")
    fields = {
        "1": ("first_name", name_check, system_admin.first_name),
        "2": ("last_name", name_check, system_admin.last_name),
        "3": ("username", validate_username, system_admin.username),
        "4": ("password", validate_password, '********')  # Mask password
    }
    
    for key, (field_name, _, current_value) in fields.items():
        print(f"{key}: {field_name} (current: {current_value})")

    field_choice = input("Enter the number of the field you want to edit: ")

    if field_choice not in fields:
        return None

    field_name, validation_func, _ = fields[field_choice]
    if field_name == "password":
        new_value = prompt_password(f"Enter new {field_name}: ", validation_func)
    else:
        new_value = get_valid_input(f"Enter new {field_name}: ", validation_func)
    
    if new_value:
        if field_choice == "4":  # Password needs to be hashed
            new_value = bcrypt.hashpw(new_value.encode(), bcrypt.gensalt()).decode()
        return field_name, new_value
    else:
        print(f"No new value was given.")
        return None

