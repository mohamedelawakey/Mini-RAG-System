from enum import Enum


# Signals returned by the API to indicate file upload/validation status
class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file type not supported"
    FILE_SIZE_EXCEEDED = "file size exceeded"
    FILE_UPLOADED_SUCCESS = "file uploaded successfully"
    FILE_UPLOADED_FAILED = "file uploaded failed"
    FILE_VALIDATED_SUCCESS = "file validated successfully"
