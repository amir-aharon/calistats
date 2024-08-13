from calistats.domain.models import Stat, StatType
from calistats.domain.repositories import StatRepository, StatTypeRepository
from calistats.infrastructure.file.base_repository import BaseFileRepository
from calistats.infrastructure.file.consts import STATS_FILE, STAT_TYPES_FILE


class FileStatTypeRepository(BaseFileRepository, StatTypeRepository):
    def __init__(self) -> None:
        super().__init__(StatType, STAT_TYPES_FILE)


class FileStatRepository(BaseFileRepository, StatRepository):
    def __init__(self):
        super().__init__(Stat, STATS_FILE)
