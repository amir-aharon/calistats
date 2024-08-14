"""
This file defines the domain models for the Calistats system.
These models represent the core entities in the system, such as Stat and StatType.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr


class StatType(BaseModel):
    id: Optional[int] = None
    name: str
    unit: str


class Stat(BaseModel):
    id: Optional[int] = None
    stat_type_id: int
    user_id: int
    value: float
    date: Optional[str] = None


class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    password: str
