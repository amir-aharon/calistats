"""
This is the main entry point for the FastAPI application.
It sets up the application and includes all routers to start the API server.
"""

from calistats.interface.main_router import main_router
from fastapi import FastAPI


app = FastAPI()

app.include_router(main_router)
