"""
This file implements the repository interface for Stat using the file-based storage.
It extends the base repository to provide specific functionality for managing Stat and StatType data.
"""

from calistats.domain.models import Stat
from calistats.domain.repositories import StatRepository
from calistats.infrastructure.file.base_repository import BaseFileRepository
from calistats.infrastructure.file.consts import STATS_FILE


class FileStatRepository(BaseFileRepository, StatRepository):
    def __init__(self):
        super().__init__(Stat, STATS_FILE)
