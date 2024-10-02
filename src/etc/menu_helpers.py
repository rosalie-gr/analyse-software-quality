from models.super_admin import SuperAdmin, SystemAdmin
from models.consultant import Consultant, Member

class MenuManager:
    def manage_consultants(user):
        print("\nManage Consultants\n"
              "[1] Add Consultant\n"
              "[2] Update Consultant\n"
              "[3] Reset Consultant Password\n"
              "[4] Delete Consultant\n"
              "[5] Go Back to Main Menu\n")
        
        choice = input("Choose an option: ")
        match choice:
            case '1':
                SystemAdmin.add_consultant(user)
            case '2':
                print("choice which consultant you want to update")
                user_list = SystemAdmin.list_users(user)
                MenuManager.print_user_list_role(user_list, 0)
                # update_consultant()
            case '3':
                reset_consultant_password()
            case '4':
                delete_consultant()
            case '5':
                return None
            case _:
                print("Invalid choice. Please try again.")
                manage_consultants(user)

    def manage_members(user):
        print("\nManage Members\n"
              "[1] Add Member\n"
              "[2] Update Member\n"
              "[3] Search Member\n"
              "[4] Delete Member\n"
              "[5] Go Back to Main Menu\n")

        choice = input("Choose an option: ")
        match choice:
            case '1':
                Consultant.add_member(user)
            case '2':
                update_member()
            case '3':
                search_member()
            case '4':
                delete_member()
            case '5':
                return None
            case _:
                print("Invalid choice. Please try again.")
                manage_members(user)

    def manage_admins(user):
        print("\n[1] Add Admin\n"
              "[2] Update Admin\n"
              "[3] Reset Admin Password\n"
              "[4] Delete Admin\n"
              "[5] Go Back to Main Menu\n")
        
        choice = input("Choose an option: ")
        match choice:
            case '1':
                SuperAdmin.add_system_admin(user)
            case '2':
                print("choice which admin you want to update")
                user_list = SystemAdmin.list_users(user)
                MenuManager.print_user_list_role(user_list, 1)
                # update_system_admin()
            case '3':
                reset_system_admin_password()
            case '4':
                delete_system_admin()
            case '5':
                return None
            case _:
                print("Invalid choice. Please try again.")
                manage_admins(user)

    # generic print, shows all users
    def print_user_list(user_list):
        if user_list:
            for user in user_list :
                print(f"ID: {user['ID']} Username: {user['Username']}, Role: {user['Role']}")
        else:
            return False
    # print users based on role
    def print_user_list_role(user_list, user_role):
        if user_list:
            for user in user_list :
                if user['Role'] == user_role:
                    print(f"ID: {user['ID']} Username: {user['Username']}, Role: {user['Role']}")
        else:
            return False