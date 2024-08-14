"""
This file implements the repository interface for Stat Type using the file-based storage.
It extends the base repository to provide specific functionality for managing Stat and StatType data.
"""

from calistats.domain.models import StatType
from calistats.domain.repositories import StatTypeRepository
from calistats.infrastructure.file.base_repository import BaseFileRepository
from calistats.infrastructure.file.consts import STAT_TYPES_FILE


class FileStatTypeRepository(BaseFileRepository, StatTypeRepository):
    def __init__(self) -> None:
        super().__init__(StatType, STAT_TYPES_FILE)
