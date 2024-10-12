import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import etc.validation_layer as iv





print(iv.get_valid_input(iv.length_check, "Enter input: ", False, True, 3, True))