from typing import List, Optional
from calistats.domain.models import StatType
from calistats.domain.repositories import StatTypeRepository
from calistats.infrastructure.supabase.base_repository import BaseSupabaseRepository
from calistats.infrastructure.supabase.consts import STAT_TYPES_TABLE
from calistats.infrastructure.supabase.database import SupabaseDatabase


class SupabaseStatTypeRepository(BaseSupabaseRepository, StatTypeRepository):
    def __init__(self) -> None:
        super().__init__(StatType, STAT_TYPES_TABLE)
