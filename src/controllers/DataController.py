# Libraries
from fastapi import UploadFile
from .BaseController import BaseController
from models import ResponseSignal
from .ProjectController import ProjectController
import re
import os


class DataController(BaseController):
    """
    Controller for handling data file operations such as validation and
    generating unique file names for uploads.
    """

    def __init__(self):
        super().__init__()
        # Size scale to convert MB to bytes
        self.size_scale = 1024 * 1024

    async def validate_uploading_file(self, file: UploadFile):
        """
        Validate uploaded file for type and size.

        Args:
            file (UploadFile): File uploaded by the user.

        Returns:
            tuple(bool, str): Validation result and corresponding signal.
        """

        # Check allowed MIME types
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        # Read file content to calculate size
        content = await file.read()
        size_bytes = len(content)

        # Reset file pointer for further use
        await file.seek(0)

        max_bytes = self.app_settings.FILE_SIZE * self.size_scale

        if size_bytes <= max_bytes:
            return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value
        else:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

    def generate_unique_name(self, orig_name: str, project_id: str):
        """
        Generate a unique file path for the uploaded file.

        Args:
            orig_name (str): Original file name.
            project_id (str): Project identifier.

        Returns:
            str: Full unique file path.
        """

        random_key = self.generate_random_strings()
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_file_name = self.det_clean_file_name(orig_file_name=orig_name)

        # Construct initial file path
        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )

        # Ensure uniqueness by regenerating if file exists
        while os.path.exists(new_file_path):
            random_key = self.generate_random_strings()
            project_path = ProjectController().get_project_path(project_id=project_id)
            cleaned_file_name = self.det_clean_file_name(orig_file_name=orig_name)
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path

    def det_clean_file_name(self, orig_file_name: str):
        """
        removing special characters and replacing spaces to clean file name

        Args:
            orig_file_name (str): Original file name.

        Returns:
            str: Cleaned file name.
        """

        # Remove non-alphanumeric characters except dot
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # Replace spaces with underscores
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
