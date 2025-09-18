from fastapi import FastAPI
from Routes import Base, data

app = FastAPI()
app.include_router(Base.base_router)
app.include_router(data.data_router)
