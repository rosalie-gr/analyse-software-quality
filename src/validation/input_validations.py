import re
from models.member import Gender, City, Member, Address
from database.db_connection import db_connection
import bcrypt
import getpass


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