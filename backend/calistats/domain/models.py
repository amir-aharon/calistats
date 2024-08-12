from typing import Optional
from pydantic import BaseModel


class Stat(BaseModel):
    id: Optional[int] = None
    name: str
    owner: int
    unit: str
    value: float
    date: str
