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
from models.user import User
from etc.encryption.database_encryption import database_encryption

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
                    view_logs(user)
                case '0':
                    print("Logging out")
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
                    view_logs(user)
                case '7':
                    admin = SystemAdmin(user[0], user[1], user[2], user[3], 0)
                    SuperAdmin.change_password(admin)
                case '0':
                    print("Logging out")
                case 'E':
                    print("Exiting the system")
                    exit()
def consultant_actions(user, choice):
        match choice:
                    case '1':
                        Consultant.add_member(user)
                    case '2':
                        update_member(user)
                    case '3':
                        search_member(user)
                    case '4':
                        Consultant.change_password(user)
                    case '0':
                        print("Logging out")
                    case 'E':
                        print("Exiting the system")
                        exit()

def main():
    #encrypt and set up the database
    database_encryption()
    db = db_connection("src/um.db")

    #ask user for username and password, check if match in database
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        # user = models.user.User(username, password)
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
