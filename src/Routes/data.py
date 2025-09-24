# Libraries
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProcessController
from models import ResponseSignal
import aiofiles
import logging
from .schemes.data import ProcessRequest

# Logger instance for error tracking
logger = logging.getLogger("uvicorn.error")

# Create an API router for data-related endpoints
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)


# Define a POST endpoint to upload files
@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str,
                      file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    """
    Upload a file for a given project.

    Args:
        project_id (str): Unique identifier of the project.
        file (UploadFile): File uploaded by the client.
        app_settings (Settings): Application settings injected by FastAPI.

    Returns:
        JSONResponse: Response containing a signal indicating
                      whether the upload was successful or failed.
    """
    # Initialize data controller
    data_controller = DataController()

    # Validate the uploaded file (type, size)
    is_valid, signal = await data_controller.validate_uploading_file(
        file=file)

    # If validation fails, return a 400 Bad Request
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": signal
            }
        )

    # Generate a unique file name and path for storage
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_name=file.filename,
        project_id=project_id
    )

    try:
        # Save the file in chunks asynchronously
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        # Log the error and return a failure response
        logger.error(f"error while uploading file {e}")
        return JSONResponse(
            content={
                "signal": ResponseSignal.FILE_UPLOADED_FAILED.value
            }
        )

    # Return a success response
    return JSONResponse(
            content={
                "signal": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
                "file_id": file_id
            }
    )


@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.PROCESSING_FAILED.value
            }
        )

    return file_chunks
