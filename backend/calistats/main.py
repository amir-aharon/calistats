from fastapi import FastAPI
from calistats.interface.routes import router as item_router

app = FastAPI()

app.include_router(item_router)
