"""
This file contains application-level use cases for the Calistats system, related to stats.
Use cases define the application's core behaviors, such as creating a new stat.
"""

from datetime import datetime
from typing import Any, Dict
from calistats.domain.models import Stat
from calistats.domain.repositories import StatRepository, StatTypeRepository


def create_stat(stat_repo: StatRepository, stat_type_repo: StatTypeRepository, stat_data: Dict[str, Any]) -> Stat:
    stat_type_id = stat_data["stat_type_id"]
    stat_type = stat_type_repo.get(stat_type_id)

    if stat_type is None:
        raise ValueError(f"Stat type with id {stat_type_id} does not exist")

    if "date" not in stat_data or stat_data["date"] is None:
        # ISO 8601 format
        stat_data["date"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    stat = Stat(**stat_data)
    stat_id = stat_repo.add(stat)
    return get_stat_by_id(stat_repo, stat_id)


def get_stat_by_id(repo: StatRepository, stat_id: int) -> Stat:
    return repo.get(stat_id)


def delete_stat_by_id(stat_repo: StatRepository, stat_id: int) -> None:
    stat_repo.delete(stat_id)
