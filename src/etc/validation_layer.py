import re
import getpass
from models.member import Gender, City, Member, Address
from database.db_connection import db_connection
import bcrypt


# Utility function for prompting input with optional sensitivity (for password-style inputs)
def get_valid_input(validation_func, prompt="Enter input: ", is_sensitive=True, detailed_message=False, attempts=3, no_attempt_limit=False):

    attempt = 0  # Initialize the attempt counter

    while no_attempt_limit or attempt < attempts:  # Infinite loop if no_attempt_limit is True
        attempt += 1

        value = getpass.getpass(prompt) if is_sensitive else input(prompt)

        if value == "":
            print("Returning to previous menu...")
            return # Return to previous menu if input is empty CHANGE THIS FUNCTION
        
        # Perform validation
        is_valid, message = validation_func(value)
        if is_valid:
            return value  # Return the valid input
        else:
            if no_attempt_limit:
                print(f"Incorrect input: {message if detailed_message else 'Invalid input.'}")
            
            else:
                print(f"Attempt {attempt}/{attempts} failed: {message if detailed_message else 'Invalid input.'}")
        
        # Check if attempts are exceeded when limit is applied
        if not no_attempt_limit and attempt >= attempts:
            break

    print("Too many failed attempts.")
    return False  # Return False after all attempts are exhausted

# Prompt for enum input (for selecting from predefined options like Gender, City, etc.)
def get_enum_input(prompt, enum, attempts=3):
    for attempt in range(attempts):
        print(prompt)
        for item in enum:
            print(f"{item.name}: {item.value}")

        value = input("Select from the above options (input the name): ").upper()
        
        if value in enum.__members__:
            return enum[value]
        else:
            print(f"Attempt {attempt + 1}/{attempts} failed. Invalid choice.")

    print("Too many failed attempts.")
    return None


# Modular password input function
def prompt_password(prompt, validation_func, attempts=3):
    return get_valid_input(validation_func, prompt, is_sensitive=True, attempts=attempts)


# Centralized validation utility
def validate_with_regex(value, pattern, error_message):
    if re.match(pattern, value):
        return True, None
    return False, error_message


# Validation functions (use centralized regex validation to ensure consistency)
def length_check(value, max_length=30):
    if len(value) <= max_length:
        return True, None
    return False, f"Input is too long! Maximum allowed length is {max_length} characters."


def is_required(value):
    if value.strip():  # Checks if the input is non-empty and contains something meaningful
        return True, None
    return False, "This field is required."


def name_check(value):
    return validate_with_regex(value, r"^[a-zA-Z\s\-\'\u00C0-\u017F]*$", 
                               "Name must only contain letters, spaces, hyphens, apostrophes, and accents.")


def number_check(value):
    return validate_with_regex(value, r'^[0-9]+$', "Input must be a number.")


def zip_code_check(value):
    return validate_with_regex(value, r'^[0-9]{4}[a-zA-Z]{2}$', 
                               "Zip code must be exactly 4 digits followed by 2 letters.")


def email_check(value):
    return validate_with_regex(value, r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', 
                               "Invalid email format.")


def phone_check(value):
    return validate_with_regex(value, r'^\+?[0-9\s\-]{7,15}$', 
                               "Phone number must be between 7 and 15 digits, and can include spaces, dashes, and an optional leading '+'.")


def validate_username(value):
    return validate_with_regex(value, r'^[a-zA-Z_][a-zA-Z0-9_.\']{7,9}$', 
                               "Username must have a length of 8-10 characters, start with a letter or underscore (_), and contain only letters, numbers, underscores (_), apostrophes ('), and periods (.).")


def validate_password(value):
    return validate_with_regex(value, r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-\+=`|\\(){}[\]:;\'<>,.?/])[A-Za-z\d~!@#$%&_\-\+=`|\\(){}[\]:;\'<>,.?/]{12,30}$',
                               "Password must be at least 12 characters long and no longer than 30 characters, and contain at least one lowercase letter, one uppercase letter, one digit, and one special character.")


def search_key_check(value):
    return validate_with_regex(value, r'^[a-zA-Z0-9\s\-\'\u00C0-\u017F]*$', 
                               "Search key must only contain letters, numbers, spaces, hyphens, apostrophes, and accents.")

