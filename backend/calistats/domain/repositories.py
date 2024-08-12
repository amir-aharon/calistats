from abc import ABC, abstractmethod
from typing import List
from calistats.domain.models import Stat


class StatRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Stat]:
        pass

    @abstractmethod
    def add(self, stat: Stat) -> None:
        pass
