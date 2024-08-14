from typing import Type, TypeVar, List, Optional
from calistats.infrastructure.supabase.database import SupabaseDatabase

T = TypeVar("T")


class BaseSupabaseRepository:
    def __init__(self, model: Type[T], table_name: str) -> None:
        self.model = model
        self.table_name = table_name
        self.db = SupabaseDatabase()

    def get(self, item_id: int) -> Optional[T]:
        data = self.db.select(self.table_name, {"id": item_id})
        if not data:
            return None
        return self.model(**data[0])

    def get_all(self) -> List[T]:
        data = self.db.select(self.table_name)
        return [self.model(**item) for item in data]

    def add(self, item: T) -> None:
        self.db.insert(self.table_name, item.model_dump())

    def delete(self, item_id: int) -> None:
        self.db.delete(self.table_name, {"id": item_id})
