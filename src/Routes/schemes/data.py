from pydantic import BaseModel
from typing import Optional


class ProcessRequest(BaseModel):
    """
    Defines a request model for file processing with configurable options:
    - file_id: unique file identifier
    - chunk_size: size of each text chunk (default 100)
    - overlap_size: overlap between chunks (default 20)
    - reset: reset flag (default 0)
    """

    file_id: str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    reset: Optional[int] = 0
