"""
This file defines dependency injection configurations for the FastAPI application.
It provides functions to retrieve instances of repositories or other dependencies.
"""

from calistats.domain.repositories import StatRepository, StatTypeRepository, UserRepository

# from calistats.infrastructure.file.stat_repository import FileStatRepository
# from calistats.infrastructure.file.stat_type_repository import FileStatTypeRepository
# from calistats.infrastructure.file.user_repository import FileUserRepository


from calistats.infrastructure.supabase.stat_repository import SupabaseStatRepository
from calistats.infrastructure.supabase.stat_type_repository import SupabaseStatTypeRepository
from calistats.infrastructure.supabase.user_repository import SupabaseUserRepository


def get_stat_repository() -> StatRepository:
    return SupabaseStatRepository()


def get_stat_type_repository() -> StatTypeRepository:
    return SupabaseStatTypeRepository()


def get_user_repository() -> UserRepository:
    return SupabaseUserRepository()
