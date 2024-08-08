import database.db_setup
import models.user
import bcrypt
import re
from database.db_connection import db_connection
from backup_system.backup_system import create_backup, restore_backup, list_backups, get_latest_backup

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


def main():
    #encrypt and set up the database
    db = db_connection("um.db")
    #ask user for username and password, check if match in database
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = models.user.User(username, password)
        if user.authenticate_user():
            user_role = user.role()
            return user_role
        else:
            print("Invalid username or password. Please try again.")



if __name__ == '__main__':
    main()
