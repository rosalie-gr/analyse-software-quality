import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import etc.validation_layer as iv
from logger.logger import logger
from models.member import City
from logger.SuspiciousActivityDetector import SuspiciousActivityDetector as SAD




# print(iv.get_valid_input(iv.length_check, "Enter input: ", False, True, 3, True))


print(iv.get_enum_input("Select from the above options", City, 1))

logger.log_activity("test", "test", "test")

logger.pretty_logs_display()