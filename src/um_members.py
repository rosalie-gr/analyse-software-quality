from etc.dependencies import Dependencies

print("Installing dependencies...")
Dependencies.install_dependencies()
print("Dependencies installed.")

import database.db_setup
import models.user
import bcrypt
import re
from database.db_connection import db_connection
import etc.validation_layer as v
from etc.login_validations import authenticate_user
from etc.menu_helpers import MenuManager
from backup_system import backup_system
from models.consultant import Consultant
from models.super_admin import SuperAdmin
from models.system_admin import SystemAdmin
from models.member import Member, Address
from models.user import User
from etc.encryption.database_encryption import database_encryption
from etc.useractions.update_users import Update_users
from logger.logger import logger

database.db_setup.db_setup("src/um.db")
import models.user

# displays the main menu based on the user's role
def display_menu(user_role):
    if user_role == 2: #models.user.Role.SUPER:
        print("\n[1] View Users\n"
              "[2] Manage Admins\n"
              "[3] Manage Consultants\n"
              "[4] Manage Member\n"
              "[5] Backup System\n"
              "[6] Restore System\n"
              "[7] View Logs\n"
              "[0] Logout\n"
              "[E] Exit the System\n")

    elif user_role == 1: #models.user.Role.SYSTEM:
        print("\n[1] View Users\n"
              "[2] Manage Consultants\n"
              "[3] Manage Members\n"
              "[4] Backup System\n"
              "[5] Restore System\n"
              "[6] View Logs\n"
              "[7] Update Password\n"
              "[0] Logout\n"
              "[E] Exit the System\n")

    elif user_role == 0: #models.user.Role.CONSULT:
        print("\n[1] Add Member\n"
              "[2] Update Member\n"
              "[3] Search Member\n"
              "[4] Update Password\n"
              "[0] Logout\n"
              "[E] Exit the System\n")

def handle_choice(user, choice):
    user_role = user[5]

    if user_role ==  2:#models.user.Role.SUPER:
        super_admin_actions(user, choice)
    elif user_role == 1: #models.user.Role.SYSTEM:
        system_admin_actions(user, choice)
    elif user_role == 0: # models.user.Role.CONSULT:
        consultant_actions(user, choice)

def super_admin_actions(user, choice):
     match choice:
                case '1':
                    # view list of users
                    user_list = SystemAdmin.list_users()
                    MenuManager.print_user_list(user_list)
                case '2':
                    MenuManager.manage_admins(user)
                case '3':
                    MenuManager.manage_consultants(user)
                case '4':
                    MenuManager.manage_members(user)
                case '5':
                    backup_system.create_backup()
                case '6':
                    backup_system.restore_backup(user)
                case '7':
                    logger.pretty_logs_display()
                    logger.log_activity(user[1], "View Logs", "Viewed logs")
                case '0':
                    print("Logging out")
                    logger.log_activity(user[1], "Logged out", "Logged out")
                case 'E':
                    # Logger.log_activity(user.username, "Exited the system", "System exited", False)
                    print("Exiting the system")
                    exit()

def system_admin_actions(user, choice):
     match choice:
                case '1':
                    # view list of users
                    user_list = SystemAdmin.list_users()
                    MenuManager.print_user_list(user_list)
                case '2':
                    MenuManager.manage_consultants(user)
                case '3':
                    MenuManager.manage_members(user)
                case '4':
                    backup_system.create_backup()
                case '5':
                    backup_system.restore_backup(user)
                case '6':
                    logger.pretty_logs_display()
                    logger.log_activity(user[1], "View Logs", "Viewed logs")
                case '7':
                    SuperAdmin.change_password(user)
                case '0':
                    print("Logging out")
                    logger.log_activity(user[1], "Logged out", "Logged out")
                case 'E':
                    print("Exiting the system")
                    exit()
def consultant_actions(user, choice):
        match choice:
                    case '1':
                        Consultant.add_member(user)
                    case '2':
                        print("choose which member you want to update")
                        member_list = Consultant.list_members()
                        MenuManager.print_members(member_list)
                        member_id = v.get_valid_input(v.number_check, 
                                                        "Enter the ID of the member you want to update, or enter 0 to go back to the main menu: ", False)
                        if member_id == '0' or member_id == None:
                            return
                        
                        # returns a list
                        member_info = Consultant.search_member_id(user, member_id)
                        if not member_info or member_info == None:
                            print("Member not found.")
                            return
                        member_address = Consultant.find_address(user, member_info["Address ID"])

                        # turn address list into an address object
                        address = Address(member_address["Street Name"], member_address["House Number"], member_address["Zip Code"], member_address["City"])

                        # turn member list & address object into a member object for the update_member function to use
                        member = Member(member_info["First Name"], member_info["Last Name"], member_info["Age"], member_info["Gender"], member_info["Weight"], address, member_info["Email"], member_info["Mobile Phone"])                             
                            
                        result = Update_users.update_member(member)

                        field_name, new_value = result

                        Consultant.update_member(user, member_id, field_name, new_value)
                    case '3':
                        search_key = v.get_valid_input(v.search_key_check, "Enter a search key, or enter 0 to go back to the main menu: ", False)
                        if search_key == '0':
                            return

                        # search for members based on the search key & print the results
                        found_members = SuperAdmin.search_member(user, search_key)
                        MenuManager.print_members(found_members)
                    case '4':
                        Consultant.change_password(user)
                    case '0':
                        print("Logging out")
                        logger.log_activity(user[1], "Logged out", "Logged out")
                    case 'E':
                        print("Exiting the system")
                        exit()

def main():
    #encrypt and set up the database
    database_encryption()
    db = db_connection("src/um.db")

    #ask user for username and password, check if match in database
    while True:
        username = v.get_valid_input(v.validate_username, "Enter your username: ", False, False, 3, True)
        password = input("Enter your password: ")
        user = authenticate_user(username, password)

        if user:
            
            if user[3] == 'super_admin':
                print(f"\nWelcome, {user[1]} {user[2]}")
            else:
                print(f"\nWelcome, {database_encryption.decrypt_data(user[1])} {database_encryption.decrypt_data(user[2])}!")
            
            while True:
                # display the correct menu for the type of user
                display_menu(user[5])

                choice = input("Choose an option: ").capitalize()
                if choice == '0':
                    break
                handle_choice(user, choice)
                if choice == 'E':
                    # log hehe
                    break
        else:
            print("Invalid username or password")



if __name__ == '__main__':
    main()
