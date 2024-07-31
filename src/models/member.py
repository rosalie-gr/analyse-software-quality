from enum import Enum

# For a member, the following data must be entered to the system:
# ● First Name and Last Name
# ● Age, Gender, Weight
# ● Address (Street name, House number (27, 27a), Zip Code (DDDDXX), City (system should generate a list of 10 city names of your choice predefined in the system)
# ● Email Address
# ● Mobile Phone (+31-6-DDDDDDDD) – only DDDDDDDD to be entered by the user

class Gender(Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    NON_BINARY = 'Non-binary'
    PREF_NOT = 'Prefer not to say'
    OTHER = 'Other'

class City(Enum):
    BG = 'Baldurs Gate'
    WATERDEEP = 'Waterdeep'
    MENZO = 'Menzoberranzan'
    NW = 'Neverwinter'
    CANDLE = 'Candlekeep'
    ELTUREL = 'Elturel'
    PHANDALIN = 'Phandalin'
    UNDER = 'The Underdark'
    APLANE = 'The Astral Plane'
    GRYM = 'Grymforge'

class Address():
    def __init__(self, street_name: str, house_number: str, zip_code: str, city: City):
        self.street_name = street_name
        self.house_number = house_number
        self.zip_code = zip_code
        self.city = city
        

class Member:
    def __init__(self, first_name: str, last_name: str, age: int, gender: Gender, weight: float, address: Address, email: str, mobile_phone: str):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.weight = weight
        self.address = address
        self.email = email
        self.mobile_phone = "+31-6-" + mobile_phone # The system will add the +31-6- prefix to the mobile phone number

    def set_registration_date(self, registration_date):
        self.registration_date = registration_date # This is the date the member was registered in the system, will be set by the set_registration_date service

    def set_membership_id(self, membership_id):
        self.membership_id = membership_id  # This is the unique identifier for the member, will be set by the set_membership_id service

