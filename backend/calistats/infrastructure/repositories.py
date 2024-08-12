from typing import List
from calistats.domain.models import Stat
from calistats.domain.repositories import StatRepository
from calistats.infrastructure.database import (
    read_stats_from_file,
    write_stats_to_file
)


class FileStatRepository(StatRepository):
    def __init__(self):
        self.stats = read_stats_from_file()
        self.next_id = self._calculate_next_id()

    def _calculate_next_id(self) -> int:
        if not self.stats:
            return 1
        return max(stat.id for stat in self.stats) + 1

    def add(self, stat: Stat) -> None:
        if stat.id is None:
            stat.id = self.next_id
            self.next_id += 1
        self.stats.append(stat)
        write_stats_to_file(self.stats)

    def get_all(self) -> List[Stat]:
        return self.stats
