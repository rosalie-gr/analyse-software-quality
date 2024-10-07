from models.super_admin import SuperAdmin, SystemAdmin
from models.consultant import Consultant, Member, User
from etc.useractions.update_users import Update_users
import etc.input_validations as v

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
                # its a little messy, i tried to move it all to modify consult info but circular import wahwah
                # for now its here, maybe it can be moved to updtae-users
                print("choice which consultant you want to update")
                user_list = SystemAdmin.list_users()
                MenuManager.print_user_list_role(user_list, 0)
                consultant_id = v.get_valid_input("Enter the ID of the consultant you want to update, or enter 0 to go back to the main menu: ", 
                                                  v.number_check)
                if consultant_id == '0':
                    return
                if consultant_id == False:
                    print("Too many wrong attempts, going back to main menu")
                    return
                
                # maybe still need to add a check if its a consultant
                consultant = User.search_user(user, consultant_id)
                print(consultant.first_name, consultant.last_name, consultant.username, consultant.password)

                result = Update_users.update_consultant(consultant)
                if result is None:
                    print("Not a valid field. going back to main menu")
                    return
                field_name, new_value = result

                SystemAdmin.modify_consultant_info(user, consultant_id, field_name, new_value)
            case '3':
                reset_consultant_password()
            case '4':
                user_list = SystemAdmin.list_users()
                for user in user_list:
                    if user['Role'] == 0:
                        print(f"ID: {user['ID']} Username: {user['Username']}, Role: {user['Role']}")
                consultant_id = v.get_valid_input("Enter the ID of the consultant you want to update, or enter 0 to go back to the main menu: ", 
                                                  v.number_check)
                if consultant_id == '0':
                    return
                if consultant_id == False:
                    print("Too many wrong attempts, going back to main menu")
                    return
                SystemAdmin.delete_consultant(user, consultant_id)
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
                user_list = SystemAdmin.list_users()
                MenuManager.print_user_list_role(user_list, 1)
                
                sys_id = v.get_valid_input("Enter the ID of the system admin you want to update, or enter 0 to go back to the main menu: ", 
                                        v.number_check)
                if sys_id == '0':
                    return
                if sys_id == False:
                    print("Too many wrong attempts, going back to main menu")
                    return
                
                # maybe still need to add a check if its a system admin
                sys =  User.search_user(user, sys_id)
                print(sys.first_name, sys.last_name, sys.username, sys.password)

                result = Update_users.update_system_admin(sys)
                if result is None:
                    print("Not a valid field. going back to main menu")
                    return
                field_name, new_value = result

                SuperAdmin.modify_system_admin_info(user, sys_id, field_name, new_value)
            case '3':
                reset_system_admin_password()
            case '4':
                user_list = SystemAdmin.list_users()
                MenuManager.print_user_list_role(user_list, 1)
                sys_id = v.get_valid_input("Enter the ID of the consultant you want to update, or enter 0 to go back to the main menu: ", 
                                                  v.number_check)
                if sys_id == '0':
                    return
                if sys_id == False:
                    print("Too many wrong attempts, going back to main menu")
                    return
                SuperAdmin.delete_system_admin(user, sys_id)
            case '5':
                return None
            case _:
                print("Invalid choice. Please try again.")
                manage_admins(user)

    # generic print, shows all users
    def print_user_list(user_list):
        if user_list:
            for user in user_list :
                print(f"ID: {user['ID']} Username: {user['Username']}, First Name: {user['First Name']}, Last Name: {user['Last Name']} Role: {user['Role']}")
        else:
            return False
    # print users based on role
    def print_user_list_role(user_list, user_role):
        if user_list:
            for user in user_list :
                if user['Role'] == user_role:
                    print(f"ID: {user['ID']} Username: {user['Username']}, First Name: {user['First Name']}, Last Name: {user['Last Name']} Role: {user['Role']}")
        else:
            return False
    
    # print members
    def print_members(member_list):
        if member_list:
            for member in member_list:
                print(f"ID: {member['ID']} First Name: {member['First Name']} Last Name: {member['Last Name']} Age: {member['Age']} Gender: {member['Gender']} Weight: {member['Weight']} Address ID: {member['Address ID']} Email: {member['Email']} Mobile Phone: {member['Mobile Phone']} Registration Date: {member['Registration Date']}")
        else:
            return False
