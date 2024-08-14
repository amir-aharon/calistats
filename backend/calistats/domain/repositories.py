"""
This file defines repository interfaces for interacting with the Stat and StatType models.
The repositories abstract the data persistence layer and define the contract for data access.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from calistats.domain.models import Stat, StatType


class StatTypeRepository(ABC):
    @abstractmethod
    def get(self, stat_type_id: int) -> Optional[StatType]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[StatType]:
        raise NotImplementedError

    @abstractmethod
    def add(self, stat_type: StatType) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, stat_type_id: int) -> None:
        raise NotImplementedError


class StatRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Stat]:
        raise NotImplementedError

    @abstractmethod
    def add(self, stat: Stat) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, stat_id: int) -> None:
        raise NotImplementedError
