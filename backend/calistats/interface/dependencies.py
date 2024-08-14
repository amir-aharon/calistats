"""
This file defines dependency injection configurations for the FastAPI application.
It provides functions to retrieve instances of repositories or other dependencies.
"""

from calistats.infrastructure.file.repositories import FileStatRepository, FileStatTypeRepository


def get_stat_repository() -> FileStatRepository:
    return FileStatRepository()


def get_stat_type_repository() -> FileStatTypeRepository:
    return FileStatTypeRepository()
