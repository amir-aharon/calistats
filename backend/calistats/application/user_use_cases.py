"""
This file contains application-level use cases for the Calistats system, related to users.
Use cases define the application's core behaviors, such as creating a new stat.
"""

from typing import Any, Dict
from calistats.domain.models import User
from calistats.domain.repositories import UserRepository


def create_user(repo: UserRepository, user_data: Dict[str, Any]) -> User:
    user = User(**user_data)
    user_id = repo.add(user)
    return get_user_by_id(repo, user_id)


def get_user_by_id(repo: UserRepository, user_id: int) -> User:
    user = repo.get(user_id)
    if user is None:
        raise ValueError(f"User with ID {user_id} does not exist")
    return user


def get_user_by_email(repo: UserRepository, email: str) -> User:
    user = repo.get_by_email(email)
    if user is None:
        raise ValueError(f"User with email {email} does not exist")
    return user


def delete_user_by_id(repo: UserRepository, user_id: int) -> None:
    user = repo.get(user_id)
    if user is None:
        raise ValueError(f"User with ID {user_id} does not exist")
    repo.delete(user_id)
