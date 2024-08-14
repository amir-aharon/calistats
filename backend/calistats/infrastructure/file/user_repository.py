"""
This file implements the repository interface for User using the file-based storage.
It extends the base repository to provide specific functionality for managing Stat and StatType data.
"""

from typing import Optional
from calistats.domain.models import User
from calistats.domain.repositories import UserRepository
from calistats.infrastructure.file.base_repository import BaseFileRepository
from calistats.infrastructure.file.consts import USERS_FILE


class FileUserRepository(BaseFileRepository, UserRepository):
    def __init__(self):
        super().__init__(User, USERS_FILE)

    def get_by_email(self, email: str) -> Optional[User]:
        return next((user for user in self.items if user.email == email), None)
