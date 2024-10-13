from enum import Enum
import re
import time
from datetime import datetime

class SuspiciousActivity(Enum):
    WEIRD_META_CHARACTERS = "Weird meta characters detected"
    FREQUENT_USERNAME_CHANGE = "Frequent username changes"
    RAPID_ACTIONS = "Rapid actions in a short timeframe"
    HIGH_FAILURE_RATE = "High failure rate"

class SuspiciousActivityDetector:

    def __init__(self, logs):
        self.log_data = logs  # Store log data
    
    def check_suspicious_meta_characters(self, input_string):
        # Check for weird meta characters in the input string (anything not alphanumeric or underscores)
        if re.search(r'[^a-zA-Z0-9_]', input_string):
            return True
        return False
    
    def check_rapid_actions(self, username):
        # Check for rapid actions in a short timeframe
        current_time = time.time()

        # Filter user logs in the last 15 seconds
        recent_logs = []
        for log in self.log_data:
            if log['Username'] == username:
                # Convert the timestamp from string to Unix time
                log_time = time.mktime(datetime.strptime(log['Timestamp'], "%Y-%m-%d %H:%M:%S").timetuple())
                if current_time - log_time <= 15:
                    recent_logs.append(log)

        # Flag if there are more than 5 actions in the last 15 seconds
        return len(recent_logs) >= 5
    
    def check_high_failure_rate(self, username):
        # Get logs for the user
        user_logs = [log for log in self.log_data if log['Username'] == username]

        # Filter for failed login attempts
        failure_logs = [log for log in user_logs if log['Description'] == 'Login failed']

        # Flag if the user has more than 5 failed attempts
        return len(failure_logs) >= 5
    
    def detect_suspicious_activity(self, username, description, additional_info):
        # Check for weird meta characters in the description
        if self.check_suspicious_meta_characters(description):
            return SuspiciousActivity.WEIRD_META_CHARACTERS
        
        # Check for rapid actions
        if self.check_rapid_actions(username):
            return SuspiciousActivity.RAPID_ACTIONS
        
        # Check for high failure rate
        if self.check_high_failure_rate(username):
            return SuspiciousActivity.HIGH_FAILURE_RATE
        
        # No suspicious activity detected
        return False
