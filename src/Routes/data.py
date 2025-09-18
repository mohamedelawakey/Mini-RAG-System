# Libraries
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController
from models import ResponseSignal
import aiofiles
import logging

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
    file_path = data_controller.generate_unique_name(
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
                "signal": ResponseSignal.FILE_UPLOADED_SUCCESS.value
            }
    )
