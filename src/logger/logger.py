from datetime import datetime
from enum import Enum
from etc.encryption.database_encryption import database_encryption
import csv
import os
import logger.SuspiciousActivityDetector as SAD
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding

class logger:
    LOG_FILE = 'src/Logs.csv'
    HEADERS = ['No.', 'Timestamp', 'Username', 'Description', 'Additional Info', 'Suspicious']

    @staticmethod
    def encrypt_message(message, public_key):
        encrypted = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted

    @staticmethod
    def decrypt_message(encrypted_message, private_key):
        decrypted = private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()

    def return_logs():
        with open(logger.LOG_FILE, 'r', newline='') as log_file:
            reader = csv.DictReader(log_file)

            # Load private key for decryption
            encryption = database_encryption()
            PRIVATE_KEY = encryption.load_private_key()

            logs = []
            for row in reader:
                log_number = logger.decrypt_message(eval(row["No."]), PRIVATE_KEY)
                timestamp = logger.decrypt_message(eval(row["Timestamp"]), PRIVATE_KEY)
                username = logger.decrypt_message(eval(row["Username"]), PRIVATE_KEY)
                description = logger.decrypt_message(eval(row["Description"]), PRIVATE_KEY)
                additional_info = logger.decrypt_message(eval(row["Additional Info"]), PRIVATE_KEY)
                suspicious = logger.decrypt_message(eval(row["Suspicious"]), PRIVATE_KEY)
                logs.append({
                    "No.": log_number,
                    "Timestamp": timestamp,
                    "Username": username,
                    "Description": description,
                    "Additional Info": additional_info,
                    "Suspicious": suspicious
                })

            return logs


    @staticmethod
    def log_activity(username, description, additional_info, input="", override_suspicious_param=None):
        if os.path.exists(logger.LOG_FILE):
            with open(logger.LOG_FILE, 'r') as log_file:
                reader = csv.DictReader(log_file)
                next_no = sum(1 for _ in reader) + 1  # Calculate next log number
        else:
            next_no = 1

        #Check if the entry is suspicious
        if override_suspicious_param is not None:
            suspicious = override_suspicious_param  

        else:
            # Initialize the SuspiciousActivityDetector
            suspicious_detector = SAD.SuspiciousActivityDetector(logger.return_logs())
            suspicious = suspicious_detector.detect_suspicious_activity(username, description, additional_info, input)

        with open(logger.LOG_FILE, 'a', newline='') as log_file:
            writer = csv.DictWriter(log_file, fieldnames=logger.HEADERS)

            # Write headers if this is the first log entry
            if next_no == 1:
                writer.writeheader()

            # Initialize encryption
            encryption = database_encryption()
            PUBLIC_KEY = encryption.load_public_key()

            # Encrypt the log data
            print(username)
            encrypted_data = {
                'No.': logger.encrypt_message(str(next_no), PUBLIC_KEY),  # Encrypt log number
                'Timestamp': logger.encrypt_message(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), PUBLIC_KEY),
                'Username': logger.encrypt_message(username, PUBLIC_KEY),
                'Description': logger.encrypt_message(description, PUBLIC_KEY),
                'Additional Info': logger.encrypt_message(additional_info, PUBLIC_KEY),
                'Suspicious': logger.encrypt_message(str(suspicious), PUBLIC_KEY)  # Convert to string for encryption
            }

            # Write the encrypted data to the log file
            writer.writerow(encrypted_data)


    @staticmethod
    def pretty_logs_display():

        if not os.path.exists(logger.LOG_FILE):
            print("No logs found.")
            return
        
        with open(logger.LOG_FILE, 'r', newline='') as log_file:
            reader = csv.DictReader(log_file)

            # Load private key for decryption
            encryption = database_encryption()
            PRIVATE_KEY = encryption.load_private_key()

            print("".ljust(120, "="))
            print("| No.   | Timestamp            | Username   | Description          | Additional Info              | Suspicious |")
            print("".ljust(120, "="))
            for row in reader:
                log_number = logger.decrypt_message(eval(row["No."]), PRIVATE_KEY)
                timestamp = logger.decrypt_message(eval(row["Timestamp"]), PRIVATE_KEY)
                username = logger.decrypt_message(eval(row["Username"]), PRIVATE_KEY)
                description = logger.decrypt_message(eval(row["Description"]), PRIVATE_KEY)
                additional_info = logger.decrypt_message(eval(row["Additional Info"]), PRIVATE_KEY)
                suspicious = logger.decrypt_message(eval(row["Suspicious"]), PRIVATE_KEY)
                print(f"| {log_number.ljust(5)} | {timestamp.ljust(20)} | {username.ljust(10)} | {description.ljust(20)} | {additional_info.ljust(28)} | {suspicious.ljust(10)} |")
            print("".ljust(120, "="))

    