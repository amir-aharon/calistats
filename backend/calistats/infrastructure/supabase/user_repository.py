from typing import Optional
from calistats.domain.models import User
from calistats.domain.repositories import UserRepository
from calistats.infrastructure.supabase.base_repository import BaseSupabaseRepository
from calistats.infrastructure.supabase.consts import USERS_TABLE


class SupabaseUserRepository(BaseSupabaseRepository, UserRepository):
    def __init__(self) -> None:
        super().__init__(User, USERS_TABLE)

    def get_by_email(self, email: str) -> Optional[User]:
        data = self.db.select(self.table_name, {"email": email})
        if not data:
            return None
        return self.model(**data[0])
