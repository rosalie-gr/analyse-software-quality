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
