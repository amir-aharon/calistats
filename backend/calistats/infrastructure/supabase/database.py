from supabase import create_client, Client
from calistats.infrastructure.supabase.consts import SUPABASE_URL, SUPABASE_KEY
from threading import Lock


class SupabaseDatabase:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def insert(self, table: str, data: dict):
        response = self.client.table(table).insert(data).execute()
        if response.status_code != 201:
            raise Exception(f"Failed to insert data: {response.data}")
        return response.data

    def select(self, table: str, filters: dict = None):
        query = self.client.table(table).select("*")
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        response = query.execute()
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.data}")
        return response.data

    def update(self, table: str, data: dict, filters: dict):
        query = self.client.table(table).update(data)
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        if response.status_code != 200:
            raise Exception(f"Failed to update data: {response.data}")
        return response.data

    def delete(self, table: str, filters: dict):
        query = self.client.table(table).delete()
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        if response.status_code != 200:
            raise Exception(f"Failed to delete data: {response.data}")
        return response.data
