import config
from fastapi import FastAPI
from controller.main import router

app = FastAPI()
app.include_router(router)
