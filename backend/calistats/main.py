"""
This is the main entry point for the FastAPI application.
It sets up the application and includes all routers to start the API server.
"""

from fastapi import FastAPI
from calistats.interface.main_router import main_router

app = FastAPI()

app.include_router(main_router)
