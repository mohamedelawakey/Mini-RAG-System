from fastapi import APIRouter, Depends
from helpers.config import get_settings, Settings

# Create a base API router with prefix and tags
base_router = APIRouter(
    prefix='/api/v1',
    tags=['api_v1'],
)


# Root endpoint for the API
@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    """
    Returns:
        dict: A dictionary containing application name and version,
              fetched from environment variables.
              Example:
              {
                  "app_name": "MyApp",
                  "app_version": "1.0.0"
              }
    """

    # Fetch environment variables for app name and version
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

    # Return app metadata as JSON response
    return {
        "app_name": app_name,
        "app_version": app_version,
    }
