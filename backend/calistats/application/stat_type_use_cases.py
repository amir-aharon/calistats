"""
This file contains application-level use cases for the Calistats system, related to stat types.
Use cases define the application's core behaviors, such as creating a new stat.
"""

from typing import Any, Dict
from calistats.domain.models import StatType
from calistats.domain.repositories import StatTypeRepository


def create_stat_type(repo: StatTypeRepository, stat_type_data: Dict[str, Any]) -> StatType:
    stat_type = StatType(**stat_type_data)
    repo.add(stat_type)
    return stat_type


def get_stat_type_by_id(repo: StatTypeRepository, stat_type_id: int) -> StatType:
    return repo.get(stat_type_id)


def delete_stat_type_by_id(repo: StatTypeRepository, stat_type_id: int) -> None:
    repo.delete(stat_type_id)
