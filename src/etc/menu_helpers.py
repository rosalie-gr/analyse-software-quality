from models.super_admin import SuperAdmin, SystemAdmin
from models.consultant import Consultant, Member, User, Address
from etc.useractions.update_users import Update_users
import etc.validation_layer as v

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
                print("Choose which consultant you want to update")
                user_list = SystemAdmin.list_users()
                MenuManager.print_user_list_role(user_list, 0)
                consultant_id = v.get_valid_input(v.number_check, 
                                                  "Enter the ID of the consultant you want to update, or enter 0 to go back to the main menu: ", False)
                if consultant_id == '0' or consultant_id == None:
                    return
                
                consultant = User.search_user(user, consultant_id)
                if not consultant or consultant == None:
                    return

                result = Update_users.update_consultant(consultant)
                if result is None:
                    return
                field_name, new_value = result

                SystemAdmin.modify_consultant_info(user, consultant_id, field_name, new_value)
            case '3':
                user_list = SystemAdmin.list_users()
                MenuManager.print_user_list_role(user_list, 0)
                consultant_id = v.get_valid_input(v.number_check, 
                                                  "Enter the ID of the consultant you want to update, or enter 0 to go back to the main menu: ", False) 
                if consultant_id == '0' or consultant_id == None:
                    return
                SystemAdmin.reset_consultant_password(user, consultant_id)
            case '4':
                user_list = SystemAdmin.list_users()
                MenuManager.print_user_list_role(user_list, 0)
                consultant_id = v.get_valid_input(v.number_check, 
                                                  "Enter the ID of the consultant you want to update, or enter 0 to go back to the main menu: ", False)
                if consultant_id == '0' or consultant_id == None:
                    return
                SystemAdmin.delete_consultant(user, consultant_id)
            case '5':
                return None
            case _:
                print("Invalid choice. Please try again.")
                MenuManager.manage_consultants(user)

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
                print("choose which member you want to update")
                member_list = Consultant.list_members()
                MenuManager.print_members(member_list)
                member_id = v.get_valid_input(v.number_check, 
                                                  "Enter the ID of the member you want to update, or enter 0 to go back to the main menu: ", False)
                if member_id == '0' or member_id == None:
                    return
                
                # returns a list
                member_info = Consultant.search_member_id(user, member_id)
                if not member_info:
                    print("Member not found.")
                    return
                member_address = Consultant.find_address(user, member_info["Address ID"])

                # turn address list into an address object
                address = Address(member_address["Street Name"], member_address["House Number"], member_address["Zip Code"], member_address["City"])

                # turn member list & address object into a member object for the update_member function to use
                member = Member(member_info["First Name"], member_info["Last Name"], member_info["Age"], member_info["Gender"], member_info["Weight"], address, member_info["Email"], member_info["Mobile Phone"])                             
                       
                result = Update_users.update_member(member)
                if result is None:
                    return

                field_name, new_value = result

                Consultant.update_member(user, member_id, field_name, new_value)
            case '3':
                search_key = v.get_valid_input(v.search_key_check, "Enter a search key, or enter 0 to go back to the main menu: ", False)
                if search_key == '0' or search_key == None:
                    return

                # search for members based on the search key & print the results
                found_members = SuperAdmin.search_member(user, search_key)
                MenuManager.print_members(found_members)
            case '4':
                print("Choose which member you want to delete")
                # get & print list of all members
                member_list = Consultant.list_members()
                MenuManager.print_members(member_list)

                # get input for a member ID to delete it
                member_id = v.get_valid_input(v.number_check, 
                                                  "Enter the ID of the member you want to update, or enter 0 to go back to the main menu: ", False)
                if member_id == '0':
                    return
                
                # search for that specific member based on their ID
                member = SuperAdmin.search_member_id(user, member_id)

                SuperAdmin.delete_member(user, member["ID"], member["Address ID"])
            case '5':
                return None
            case _:
                print("Invalid choice. Please try again.")
                MenuManager.manage_members(user)

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
                print("choose which admin you want to update")
                user_list = SystemAdmin.list_users()
                MenuManager.print_user_list_role(user_list, 1)
                
                sys_id = v.get_valid_input(v.number_check, 
                                           "Enter the ID of the admin you want to update, or enter 0 to go back to the main menu: ", False)
                if sys_id == None or sys_id == '0':
                    return
                
                sys =  User.search_user(user, sys_id)
                if not sys or sys == None:
                    return

                result = Update_users.update_system_admin(sys)
                if result is None:
                    return
                field_name, new_value = result

                SuperAdmin.modify_system_admin_info(user, sys_id, field_name, new_value)
            case '3':
                user_list = SystemAdmin.list_users()
                MenuManager.print_user_list_role(user_list, 1)
                sys_id = v.get_valid_input(v.number_check, 
                                           "Enter the ID of the admin you want to update, or enter 0 to go back to the main menu: ", False)
                if sys_id == '0':
                    return
                SuperAdmin.reset_system_admin_password(user, sys_id)
            case '4':
                user_list = SystemAdmin.list_users()
                MenuManager.print_user_list_role(user_list, 1)
                sys_id = v.get_valid_input(v.number_check, 
                                           "Enter the ID of the admin you want to update, or enter 0 to go back to the main menu: ", False)
                if sys_id == '0':
                    return
                SuperAdmin.delete_system_admin(user, sys_id)
            case '5':
                return None
            case _:
                print("Invalid choice. Please try again.")
                MenuManager.manage_admins(user)

    # generic print, shows all users
    def print_user_list(user_list):
        if user_list:
            for user in user_list :
                print(f"ID: {user['ID']} Username: {user['Username']}, First Name: {user['First Name']}, Last Name: {user['Last Name']} Role: {user['Role']}")
        else:
            print("No users found.")
            return False
    # print users based on role
    def print_user_list_role(user_list, user_role):
        if user_list:
            for user in user_list :
                if user['Role'] == user_role:
                    print(f"ID: {user['ID']} Username: {user['Username']}, First Name: {user['First Name']}, Last Name: {user['Last Name']} Role: {user['Role']}")
        else:
            print("No users found with that role.")
            return False
    
    # print members
    def print_members(member_list):
        if member_list:
            for member in member_list:
                print(f"ID: {member['ID']} First Name: {member['First Name']} Last Name: {member['Last Name']} Age: {member['Age']} Gender: {member['Gender']} Weight: {member['Weight']} Address ID: {member['Address ID']} Email: {member['Email']} Mobile Phone: {member['Mobile Phone']} Registration Date: {member['Registration Date']}")
        else:
            return False
