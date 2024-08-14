"""
This file defines dependency injection configurations for the FastAPI application.
It provides functions to retrieve instances of repositories or other dependencies.
"""

from calistats.infrastructure.file.stat_repository import FileStatRepository
from calistats.infrastructure.file.stat_type_repository import FileStatTypeRepository
from calistats.infrastructure.file.user_repository import FileUserRepository


def get_stat_repository() -> FileStatRepository:
    return FileStatRepository()


def get_stat_type_repository() -> FileStatTypeRepository:
    return FileStatTypeRepository()


def get_user_repository() -> FileUserRepository:
    return FileUserRepository()
