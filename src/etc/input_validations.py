import re
import getpass
from models.member import Gender, City, Member, Address
from database.db_connection import db_connection
import bcrypt


class ValidationError(Exception):
    
    def __init__(self, message, detailed=False, errors=None):
        super().__init__(message)

        if errors is None:
            errors = []

        self.errors = errors

    def __str__(self):
        
        if self.errors & self.detailed == True:  
            return f"{self.args[0]}: {', '.join(self.errors)}"
        
        elif self.errors & self.detailed == False:
            return self.args[0]

        return self.args[0]

class Validator:
    def __init__(self):
        self.errors = []

    def validate(self, data, rules):
        for field, validations in rules.items():
            value = data.get(field)
            for validation in validations:
                try:
                    validation(value)
                except ValidationError as e:
                    self.errors.append(f"{field}: {str(e)}")
        
        if self.errors:
            raise ValidationError("Validation failed", self.errors)

    def clear_errors(self):
        self.errors.clear()

# General input functions
def get_valid_input(prompt, validation_func):
    return prompt_for_valid_input(prompt, validation_func)

def prompt_for_valid_input(prompt, validation_func):
    attempts = 0
    while attempts < 3:
        value = input(prompt)
        if validation_func(value):
            return value
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
        attempts += 1
        print(f"Attempt {attempts}/3 failed. Try again.")
    print("\nToo many failed attempts.")
    return False

def get_enum_input(prompt, enum):
    attempts = 0
    while attempts < 3:
        print(prompt)
        for item in enum:
            print(f"{item.name}: {item.value}")
        value = input("Select from the above options (input from the first column): ").upper()
        if value in enum.__members__:
            return enum[value]
        attempts += 1
        print(f"Attempt {attempts}/3 failed. Try again.")
    print("Too many failed attempts.")
    return None

# Validation functions
def length_check(value):
    if len(value) > 30:
        raise ValidationError("Input is too long! Maximum allowed length is 30.")
    return True

def is_required(value):
    if not value:
        raise ValidationError("This field is required.")
    return True

def name_check(value):
    if re.match(r"^[a-zA-Z\s\-\'\u00C0-\u017F]*$", value):
        return True
    raise ValidationError("Input must contain only letters, spaces, hyphens, apostrophes, and accents.")

def number_check(value):
    if re.match(r'^[0-9]*$', value):
        return True
    raise ValidationError("Input must be a number.")

def zip_code_check(value):
    if re.match(r'^[0-9]{4}[a-zA-Z]{2}$', value):
        return True
    raise ValidationError("Zip code must be exactly 4 digits followed by 2 letters.")

def email_check(value):
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        return True
    raise ValidationError("Invalid email format.")

def phone_check(value):
    if re.match(r'^\+?[0-9\s\-]{7,15}$', value):
       return True
    raise ValidationError("Phone number must be between 7 and 15 digits, and can include spaces, dashes, and an optional leading '+'.")

def validate_username(value):
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_.\']{7,9}$', value):
        return True
    raise ValidationError("Username must have a length of 8-10 characters, start with a letter or underscore (_), and contain only letters, numbers, underscores (_), apostrophes ('), and periods (.).")

def validate_password(value):
    if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-\+=`|\\(){}[\]:;\'<>,.?/])[A-Za-z\d~!@#$%&_\-\+=`|\\(){}[\]:;\'<>,.?/]{12,30}$', value):
        return True
    raise ValidationError("Password must be at least 12 characters long and no longer than 30 characters, and contain at least one lowercase letter, one uppercase letter, one digit, and one special character.")

def search_key_check(value):
    if re.match(r'^[a-zA-Z0-9\s\-\'\u00C0-\u017F]*$', value):
        return True
    raise ValidationError("Search key must only contain letters, numbers, spaces, hyphens, apostrophes, and accents.")


# Example usage

# data = {
#     'name': 'John Doe',
#     'age': '-25',
#     'email': 'johndoe@example.com',
#     'username': 'John_Doe1',
#     'password': 'Password123!',
#     'zip_code': '1234AB',
#     'phone': '+1234567890'
# }

# rules = {
#     'name': [is_required, name_check, length_check],
#     'age': [is_required, number_check],
#     'email': [is_required, email_check],
#     'username': [is_required, validate_username],
#     'password': [is_required, validate_password],
#     'zip_code': [is_required, zip_code_check],
#     'phone': [is_required, phone_check],
# }

# validator = Validator()

# try:
#     validator.validate(data, rules)
# except ValidationError as e:
#     print("Validation errors occurred:", e.args[1])
