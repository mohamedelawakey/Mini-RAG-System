from enum import Enum


class ProcessingEnumerations(Enum):
    """
    Defines an enum for supported file formats (TXT, PDF).
    Ensures consistency when handling file types.
    """
    TXT = ".txt"
    PDF = ".pdf"
