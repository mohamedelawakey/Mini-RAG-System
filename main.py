from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv('assets/.env')

from Routes import base

app = FastAPI()
app.include_router(base.base_router)
