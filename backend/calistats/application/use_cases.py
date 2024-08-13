from typing import Any, Dict
from calistats.domain.models import Stat, StatType
from calistats.domain.repositories import StatRepository, StatTypeRepository


def create_stat(repo: StatRepository, stat_data: Dict[str, Any]) -> Stat:
    stat = Stat(**stat_data)
    repo.add(stat)
    return stat


def create_stat_type(repo: StatTypeRepository, stat_type_data: Dict[str, Any]) -> StatType:
    stat_type = StatType(**stat_type_data)
    repo.add(stat_type)
    return stat_type


def get_stat_type(repo: StatTypeRepository, stat_type_id: int) -> StatType:
    return repo.get(stat_type_id)
