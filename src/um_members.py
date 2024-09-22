import database.db_setup
import models.user
import bcrypt
import re
from database.db_connection import db_connection
import validation.input_validations, validation.login_validations
from helpers import menu_helpers
from backup_system import backup_system

database.db_setup.db_setup("um.db")
import models.user

# displays the main menu based on the user's role
def display_menu(user_role):
    if user_role == models.user.Role.SUPER:
        print("\n[1] View Users\n"
              "[2] Manage Admins\n"
              "[3] Manage Consultants\n"
              "[4] Manage Members\n"
              "[5] Search Member\n"
              "[6] Backup System\n"
              "[7] Restore System\n"
              "[8] View Logs\n"
              "[0] Logout\n"
              "[E] Exit the System\n")

    elif user_role == models.user.Role.SYSTEM:
        print("\n[1] View Users\n"
              "[2] Manage Consultants\n"
              "[3] Manage Members\n"
              "[4] Search Member\n"
              "[5] Backup System\n"
              "[6] Restore System\n"
              "[7] View Logs\n"
              "[8] Update Password\n"
              "[0] Logout\n"
              "[E] Exit the System\n")

    elif user_role == models.user.Role.CONSULT:
        print("\n[1] Add Member\n"
              "[2] Update Member\n"
              "[3] Search Member\n"
              "[4] Update Password\n"
              "[0] Logout\n"
              "[E] Exit the System\n")

def handle_choice(user, choice):
    user_role = user.role

    if user_role == models.user.Role.SUPER:
        super_admin_actions(user, choice)
    elif user_role == models.user.Role.SYSTEM:
        system_admin_actions(user, choice)
    elif user_role == models.user.Role.CONSULT:
        consultant_actions(user, choice)

def super_admin_actions(user, choice):
     match choice:
                case '1':
                    view_users(user)
                case '2':
                    menu_helpers.manage_admins(user)
                case '3':
                    menu_helpers.manage_consultants(user)
                case '4':
                    menu_helpers.manage_members(user)
                # case '5':
                #     search_member(user)
                case '6':
                    backup_system.create_backup(user)
                case '7':
                    #this might need to be updated to list all backups first and then ask for the backup to restore, also show latest backup
                    backup_system.restore_backup(user)
                case '8':
                    view_logs(user)
                case '0':
                    print("Logging out")
                    # Handle logout logic
                case 'E':
                    Logger.log_activity(user.username, "Exited the system", "System exited", False)
                    print("Exiting the system")
                    # Handle exit logic

def system_admin_actions(user, choice):
     match choice:
                case '1':
                    view_users(user)
                case '2':
                    menu_helpers.manage_consultants(user)
                case '3':
                    menu_helpers.manage_members(user)
                # case '4':
                #     search_member(user)
                case '5':
                    backup_system.create_backup(user)
                case '6':
                    #this might need to be updated to list all backups first and then ask for the backup to restore, also show latest backup
                    backup_system.restore_backup(user)
                case '7':
                    view_logs(user)
                case '0':
                    print("Logging out")
                    # Handle logout logic
                case 'E':
                    print("Exiting the system")
def consultant_actions(user, choice):
        match choice:
                    case '1':
                        add_member(user)
                    case '2':
                        update_member(user)
                    case '3':
                        search_member(user)
                    case '4':
                        update_password(user)
                    case '0':
                        print("Logging out")
                        # Handle logout logic
                    case 'E':
                        print("Exiting the system")

def main():
    #encrypt and set up the database
    db = db_connection("um.db")
    #ask user for username and password, check if match in database
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = models.user.User(username, password)
        if validation.authenticate_user(username, password):
            user_role = user.role()
            return user_role
        else:
            print("Invalid username or password. Please try again.")



if __name__ == '__main__':
    main()
