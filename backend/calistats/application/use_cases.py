"""
This file contains application-level use cases for the Calistats system.
Use cases define the application's core behaviors, such as creating a new stat.
"""

from datetime import datetime
from typing import Any, Dict
from calistats.domain.models import Stat, StatType
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
    stat_repo.add(stat)
    return stat


def delete_stat(stat_repo: StatRepository, stat_id: int) -> None:
    stat_repo.delete(stat_id)


def create_stat_type(repo: StatTypeRepository, stat_type_data: Dict[str, Any]) -> StatType:
    stat_type = StatType(**stat_type_data)
    repo.add(stat_type)
    return stat_type


def get_stat_type(repo: StatTypeRepository, stat_type_id: int) -> StatType:
    return repo.get(stat_type_id)


def delete_stat_type(repo: StatTypeRepository, stat_type_id: int) -> None:
    repo.delete(stat_type_id)
