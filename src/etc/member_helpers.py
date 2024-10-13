import random
import datetime

class member_helper:
    def get_registration_date():
        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.month
        day = current_date.day
        date_string = f"{year:04d}-{month:02d}-{day:02d}"
        return date_string

    def get_membership_id():
        
        while True:
            current_year = datetime.datetime.now().year
            last_two_digits = str(current_year)[-2:]
            print("Year:", last_two_digits)
            
            random_digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])
            
            id_without_checksum = last_two_digits + random_digits

            checksum = sum(int(digit) for digit in id_without_checksum) % 10
            
            final_id = id_without_checksum + str(checksum)
            print(final_id)
            return final_id
