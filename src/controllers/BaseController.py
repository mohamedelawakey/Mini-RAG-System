from helpers.config import get_settings
import os
import random
import string


class BaseController:
    """
    Base controller providing common utilities for other controllers,
    such as application settings, base paths, and helper functions.
    """

    def __init__(self):
        # Load application settings
        self.app_settings = get_settings()
        # Base directory of the project
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        # Directory to store uploaded files
        self.file_dir = os.path.join(self.base_dir, "assets/files")

    def generate_random_strings(self, length: int = 12):
        # Generate a random alphanumeric string of given length
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
