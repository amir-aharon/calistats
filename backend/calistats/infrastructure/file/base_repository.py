from typing import List, Optional, Type, TypeVar
from calistats.infrastructure.file.database import (
    read_from_file,
    write_to_file
)

T = TypeVar('T')


class BaseFileRepository:
    def __init__(self, model: Type[T], file_path: str) -> None:
        self.model = model
        self.file_path = file_path
        self.items = read_from_file(self.file_path, self.model)
        self.next_id = self._calculate_next_id()

    def _calculate_next_id(self) -> int:
        if not self.items:
            return 1
        return max(item.id for item in self.items) + 1

    def get(self, item_id: int) -> Optional[T]:
        return next((item for item in self.items if item.id == item_id), None)

    def get_all(self) -> List[T]:
        return self.items

    def add(self, item: T) -> None:
        if item.id is None:
            item.id = self.next_id
            self.next_id += 1
        self.items.append(item)
        write_to_file(self.file_path, self.items)
