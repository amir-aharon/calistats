# calistats/infrastructure/supabase/database.py

from supabase import create_client, Client
from typing import Optional, Dict, List, Any
from calistats.infrastructure.supabase.consts import SUPABASE_URL, SUPABASE_KEY
from threading import Lock


class SupabaseDatabase:
    _instance: Optional["SupabaseDatabase"] = None
    _lock: Lock = Lock()

    def __new__(cls) -> "SupabaseDatabase":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_client()
        return cls._instance

    def _init_client(self) -> None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Supabase URL and Key must be provided.")
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        if "id" in data:
            del data["id"]  # Ensure the ID is not included in the insert operation
        response = self.client.table(table).insert(data).execute()
        return response.data[0]["id"]

    def select(self, table: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        query = self.client.table(table).select("*")
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        response = query.execute()
        return response.data

    def delete(self, table: str, filters: Dict[str, Any]) -> int:
        query = self.client.table(table).delete()
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        return response.count
