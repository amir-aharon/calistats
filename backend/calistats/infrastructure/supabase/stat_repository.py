from calistats.domain.models import Stat
from calistats.domain.repositories import StatRepository
from calistats.infrastructure.supabase.base_repository import BaseSupabaseRepository
from calistats.infrastructure.supabase.consts import STATS_TABLE


class SupabaseStatRepository(BaseSupabaseRepository, StatRepository):
    def __init__(self) -> None:
        super().__init__(Stat, STATS_TABLE)
