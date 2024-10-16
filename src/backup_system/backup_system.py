import os
import zipfile
import shutil
from datetime import datetime
import etc.validation_layer as v
from logger.logger import logger

# Ensure these paths are correct relative to the script location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATABASE_FILE should be one level above BASE_DIR
DATABASE_FILE = os.path.join(os.path.dirname(BASE_DIR), 'src/um.db')
LOG_FILES_DIR = os.path.join(BASE_DIR)
BACKUP_DIR = os.path.join(BASE_DIR, r"backup_system\backups")

def create_backup():
    print(BASE_DIR)
    print(DATABASE_FILE)
    # Ensure the backup directory exists
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    # Create a unique backup filename based on the current date and time
    backup_filename = os.path.join(BACKUP_DIR, f'backup_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.zip')

    # Create a zip file
    with zipfile.ZipFile(backup_filename, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
        # Add the database file to the zip
        if os.path.exists(DATABASE_FILE):
            backup_zip.write(DATABASE_FILE, os.path.basename(DATABASE_FILE))
        else:
            print(f'Database file {DATABASE_FILE} does not exist.')

        # Add log file to the zip
        for root, _, files in os.walk(LOG_FILES_DIR):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    backup_zip.write(file_path, os.path.relpath(file_path, LOG_FILES_DIR))
    
    print(f'Backup created successfully: {backup_filename}')


def restore_backup(user):
    list = list_backups()
    for i in range(len(list)):
        print(f"{i+1}. {list[i]}")
        # later check if nummer with value is in list

    while True:
        backup_file = v.get_valid_input(v.number_check, "Enter the number of the backup you want to restore: ", False, True, 1, True)

        if int(backup_file) > len(list) or int(backup_file) < 1:
            print("Invalid backup number. Please try again.")
            continue

        elif int(backup_file) <= len(list):
            break


    backup_file = list[int(backup_file)-1]
    print(f"Restoring backup: {backup_file}")
    
    # Ensure the backup file exists
    backup_file = os.path.join(BACKUP_DIR, backup_file)
    if not os.path.exists(backup_file):
        print(f'Backup file {backup_file} does not exist.')
        return
    
    # Extract the backup file to a temporary location
    temp_restore_dir = os.path.join(BACKUP_DIR, 'temp')
    if not os.path.exists(temp_restore_dir):
        os.makedirs(temp_restore_dir)
    
    with zipfile.ZipFile(backup_file, 'r') as backup_zip:
        backup_zip.extractall(temp_restore_dir)
    
    # Restore the database and log files to their correct locations
    restored_files = backup_zip.namelist()
    for file in restored_files:
        file_path = os.path.join(temp_restore_dir, file)
        
        # Restore the database file
        if os.path.basename(file) == os.path.basename(DATABASE_FILE):
            shutil.copy(file_path, DATABASE_FILE)
            print('Database restored successfully.')
        
        # Restore log files
        elif file.endswith('.csv'):
            log_file_path = os.path.join(LOG_FILES_DIR, os.path.basename(file))
            if os.path.exists(log_file_path):
                os.remove(log_file_path)  # Remove the existing log file
            shutil.copy(file_path, log_file_path)
            print(f'Log file restored successfully: {file}')
    
    # Clean up the temporary restore directory
    shutil.rmtree(temp_restore_dir)
    
    print('System restored successfully.')
    logger.log_activity(user[3], "Restore Backup", f"Restored system from backup {backup_file}")


def list_backups():
    backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.zip')]
    backups.sort(reverse=True)
    return backups

def get_latest_backup():
    available_backups = list_backups()
    if available_backups:
        print(f'Latest backup: {available_backups[0]}')
        return os.path.join(BACKUP_DIR, available_backups[0])
    else:
        return None
