import re
from datetime import timedelta
from datetime import datetime

class SuspiciousActivityDetector:

    def __init__(self, logs):
        self.log_data = logs  # Store log data
    
    def check_SQL_injection_attempt(self, input_string):
        if re.search(r'(;|--)', input_string):
            return True
        
    def shell_injection_attempt(self, input_string):
        if re.search(r'(\||;|\$|\(|\)|`)', input_string):
            return True
    
    def null_byte_injection_attempt(self, input_string):
        if re.search(r'(\x00)', input_string):
            return True  
        

    def high_number_of_requests(self, username):
        current_time = datetime.now()
        time_threshold = current_time - timedelta(minutes=1)
        
        timestamp_format = "%Y-%m-%d %H:%M:%S"  
        
        request_count = sum(1 for log in self.log_data 
                            if log['Username'] == username 
                            and datetime.strptime(log['Timestamp'], timestamp_format) >= time_threshold)
        
        return request_count > 10

    def high_number_of_failed_attempts(self, username):
        current_time = datetime.now()
        time_threshold = current_time - timedelta(minutes=1)
        
        timestamp_format = "%Y-%m-%d %H:%M:%S"  
        
        failed_attempt_count = sum(1 for log in self.log_data 
                                if log['Username'] == username 
                                and 'Failed Login Attempt' in log['Description'] 
                                and datetime.strptime(log['Timestamp'], timestamp_format) >= time_threshold)
        
        return failed_attempt_count > 5

    
    def detect_suspicious_activity(self, username, description, additional_info, input=""):

        if input != None and input != False:
            if self.check_SQL_injection_attempt(input):
                return "True - SQL Injection Attempt"
            elif self.shell_injection_attempt(input):
                return "True - Shell Injection Attempt"
            elif self.null_byte_injection_attempt(input):
                return "True - Null Byte Injection Attempt"
            
        elif self.high_number_of_requests(username):
            return "True - High Number of Requests"
        elif self.high_number_of_failed_attempts(username):
            return "True - High Number of Failed Login Attempts"	
        else:
            return False # No suspicious activity detected

