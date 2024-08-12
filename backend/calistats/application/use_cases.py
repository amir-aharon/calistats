from typing import Any, Dict
from calistats.domain.models import Stat
from calistats.domain.repositories import StatRepository


def create_stat(repo: StatRepository, stat_data: Dict[str, Any]) -> Stat:
    stat = Stat(**stat_data)
    repo.add(stat)
    return stat
