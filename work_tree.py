# calistats/application/stat_type_use_cases.py
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

# calistats/application/stat_use_cases.py
"""
This file contains application-level use cases for the Calistats system, related to stats.
Use cases define the application's core behaviors, such as creating a new stat.
"""

from datetime import datetime
from typing import Any, Dict
from calistats.domain.models import Stat
from calistats.domain.repositories import StatRepository, StatTypeRepository


def create_stat(stat_repo: StatRepository, stat_type_repo: StatTypeRepository, stat_data: Dict[str, Any]) -> Stat:
    stat_type_id = stat_data["stat_type_id"]
    stat_type = stat_type_repo.get(stat_type_id)

    if stat_type is None:
        raise ValueError(f"Stat type with id {stat_type_id} does not exist")

    if "date" not in stat_data or stat_data["date"] is None:
        # ISO 8601 format
        stat_data["date"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    stat = Stat(**stat_data)
    stat_repo.add(stat)
    return stat


def get_stat_by_id(repo: StatRepository, stat_id: int) -> Stat:
    return repo.get(stat_id)


def delete_stat_by_id(stat_repo: StatRepository, stat_id: int) -> None:
    stat_repo.delete(stat_id)

# calistats/application/user_use_cases.py
"""
This file contains application-level use cases for the Calistats system, related to users.
Use cases define the application's core behaviors, such as creating a new stat.
"""

from typing import Any, Dict
from calistats.domain.models import User
from calistats.domain.repositories import UserRepository


def create_user(repo: UserRepository, user_data: Dict[str, Any]) -> User:
    user = User(**user_data)
    repo.add(user)
    return user


def get_user_by_id(repo: UserRepository, user_id: int) -> User:
    user = repo.get(user_id)
    if user is None:
        raise ValueError(f"User with ID {user_id} does not exist")
    return user


def get_user_by_email(repo: UserRepository, email: str) -> User:
    user = repo.get_by_email(email)
    if user is None:
        raise ValueError(f"User with email {email} does not exist")
    return user


def delete_user_by_id(repo: UserRepository, user_id: int) -> None:
    user = repo.get(user_id)
    if user is None:
        raise ValueError(f"User with ID {user_id} does not exist")
    repo.delete(user_id)

# calistats/domain/models.py
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

# calistats/domain/repositories.py
"""
This file defines repository interfaces for interacting with the Stat and StatType models.
The repositories abstract the data persistence layer and define the contract for data access.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from calistats.domain.models import Stat, StatType, User


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
    def get(self, stat_type_id: int) -> Optional[StatType]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Stat]:
        raise NotImplementedError

    @abstractmethod
    def add(self, stat: Stat) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, stat_id: int) -> None:
        raise NotImplementedError


class UserRepository(ABC):
    @abstractmethod
    def get(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass

# calistats/infrastructure/file/base_repository.py
"""
This file contains a base repository implementation for working with JSON files.
It provides common functionality for file-based repositories, such as reading and writing data.
"""

from typing import List, Optional, Type, TypeVar
from calistats.infrastructure.file.database import read_from_file, write_to_file

T = TypeVar("T")


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

    def delete(self, item_id: int) -> None:
        self.items = [item for item in self.items if item.id != item_id]
        write_to_file(self.file_path, self.items)

# calistats/infrastructure/file/consts.py
"""
This file defines constants used across the file-based infrastructure, such as file paths.
"""

STATS_FILE = "stats.json"
STAT_TYPES_FILE = "stat_types.json"
USERS_FILE = "users.json"

# calistats/infrastructure/file/database.py
"""
This file provides utility functions for reading and writing Stat and StatType data from JSON files.
It acts as a data access layer specifically for file-based storage.
"""

import json
from typing import List, Type, TypeVar
from pathlib import Path

T = TypeVar("T")


def read_from_file(file_name: str, model: Type[T]) -> List[T]:
    path = Path(Path(__file__).parent, "resources", file_name)
    try:
        with path.open("r") as file:
            data = json.load(file)
        return [model(**item) for item in data]
    except Exception:
        with path.open("w") as file:
            json.dump([], file)
            return []


def write_to_file(file_name: str, items: List[T]) -> None:
    path = Path(Path(__file__).parent, "resources", file_name)
    with path.open("w") as file:
        json.dump([item.model_dump() for item in items], file, indent=4)

# calistats/infrastructure/file/resources/stats.json
[]
# calistats/infrastructure/file/resources/stat_types.json
[]
# calistats/infrastructure/file/stat_repository.py
"""
This file implements the repository interface for Stat using the file-based storage.
It extends the base repository to provide specific functionality for managing Stat and StatType data.
"""

from calistats.domain.models import Stat
from calistats.domain.repositories import StatRepository
from calistats.infrastructure.file.base_repository import BaseFileRepository
from calistats.infrastructure.file.consts import STATS_FILE


class FileStatRepository(BaseFileRepository, StatRepository):
    def __init__(self):
        super().__init__(Stat, STATS_FILE)

# calistats/infrastructure/file/stat_type_repository.py
"""
This file implements the repository interface for Stat Type using the file-based storage.
It extends the base repository to provide specific functionality for managing Stat and StatType data.
"""

from calistats.domain.models import StatType
from calistats.domain.repositories import StatTypeRepository
from calistats.infrastructure.file.base_repository import BaseFileRepository
from calistats.infrastructure.file.consts import STAT_TYPES_FILE


class FileStatTypeRepository(BaseFileRepository, StatTypeRepository):
    def __init__(self) -> None:
        super().__init__(StatType, STAT_TYPES_FILE)

# calistats/infrastructure/file/user_repository.py
"""
This file implements the repository interface for User using the file-based storage.
It extends the base repository to provide specific functionality for managing Stat and StatType data.
"""

from typing import Optional
from calistats.domain.models import User
from calistats.domain.repositories import UserRepository
from calistats.infrastructure.file.base_repository import BaseFileRepository
from calistats.infrastructure.file.consts import USERS_FILE


class FileUserRepository(BaseFileRepository, UserRepository):
    def __init__(self):
        super().__init__(User, USERS_FILE)

    def get_by_email(self, email: str) -> Optional[User]:
        return next((user for user in self.items if user.email == email), None)

# calistats/infrastructure/supabase/base_repository.py
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

# calistats/infrastructure/supabase/consts.py
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

USERS_TABLE = "users"
STATS_TABLE = "stats"
STAT_TYPES_TABLE = "stat_types"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# calistats/infrastructure/supabase/database.py
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
        if "id" in data:
            del data["id"]
        response = self.client.table(table).insert(data).execute()
        return response.data

    def select(self, table: str, filters: dict = None):
        query = self.client.table(table).select("*")
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        response = query.execute()
        return response.data

    def delete(self, table: str, filters: dict):
        query = self.client.table(table).delete()
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        return response.data

# calistats/infrastructure/supabase/stat_repository.py
from calistats.domain.models import Stat
from calistats.domain.repositories import StatRepository
from calistats.infrastructure.supabase.base_repository import BaseSupabaseRepository
from calistats.infrastructure.supabase.consts import STATS_TABLE


class SupabaseStatRepository(BaseSupabaseRepository, StatRepository):
    def __init__(self) -> None:
        super().__init__(Stat, STATS_TABLE)

# calistats/infrastructure/supabase/stat_type_repository.py
from calistats.domain.models import StatType
from calistats.domain.repositories import StatTypeRepository
from calistats.infrastructure.supabase.base_repository import BaseSupabaseRepository
from calistats.infrastructure.supabase.consts import STAT_TYPES_TABLE


class SupabaseStatTypeRepository(BaseSupabaseRepository, StatTypeRepository):
    def __init__(self) -> None:
        super().__init__(StatType, STAT_TYPES_TABLE)

# calistats/infrastructure/supabase/user_repository.py
from typing import Optional
from calistats.domain.models import User
from calistats.domain.repositories import UserRepository
from calistats.infrastructure.supabase.base_repository import BaseSupabaseRepository
from calistats.infrastructure.supabase.consts import USERS_TABLE


class SupabaseUserRepository(BaseSupabaseRepository, UserRepository):
    def __init__(self) -> None:
        super().__init__(User, USERS_TABLE)

    def get_by_email(self, email: str) -> Optional[User]:
        data = self.db.select(self.table_name, {"email": email})
        if not data:
            return None
        return self.model(**data[0])

# calistats/interface/dependencies.py
"""
This file defines dependency injection configurations for the FastAPI application.
It provides functions to retrieve instances of repositories or other dependencies.
"""

from calistats.domain.repositories import StatRepository, StatTypeRepository, UserRepository

# from calistats.infrastructure.file.stat_repository import FileStatRepository
# from calistats.infrastructure.file.stat_type_repository import FileStatTypeRepository
# from calistats.infrastructure.file.user_repository import FileUserRepository


from calistats.infrastructure.supabase.stat_repository import SupabaseStatRepository
from calistats.infrastructure.supabase.stat_type_repository import SupabaseStatTypeRepository
from calistats.infrastructure.supabase.user_repository import SupabaseUserRepository


def get_stat_repository() -> StatRepository:
    return SupabaseStatRepository()


def get_stat_type_repository() -> StatTypeRepository:
    return SupabaseStatTypeRepository()


def get_user_repository() -> UserRepository:
    return SupabaseUserRepository()

# calistats/interface/main_router.py
"""
This file defines the main API router for the FastAPI application.
It includes and organizes various route modules under a unified API structure.
"""

from fastapi import APIRouter
from calistats.interface.routes.user_routes import user_router
from calistats.interface.routes.stat_routes import stat_router
from calistats.interface.routes.stat_type_routes import stat_type_router


main_router = APIRouter()

main_router.include_router(stat_router)
main_router.include_router(stat_type_router)
main_router.include_router(user_router)

# calistats/interface/routes/stat_routes.py
"""
This file defines the API routes for managing Stat entities.
It provides endpoints for creating, retrieving, listing, and deleting stats.
"""

from calistats.application.stat_use_cases import create_stat, get_stat_by_id, delete_stat_by_id
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from calistats.interface.dependencies import get_stat_repository, get_stat_type_repository

stat_router = APIRouter()


class CreateStatRequest(BaseModel):
    user_id: int
    stat_type_id: int
    value: float


class StatResponse(BaseModel):
    id: int
    user_id: int
    stat_type_id: int
    value: float
    date: str


@stat_router.get("/stats/", response_model=list[StatResponse], tags=["Stats"])
def get_all_stats_route(repo=Depends(get_stat_repository)):
    return repo.get_all()


@stat_router.get("/stats/{stat_id}", response_model=StatResponse, tags=["Stats"])
def get_stat_route(stat_id: int, repo=Depends(get_stat_repository)):
    stat = get_stat_by_id(repo, stat_id)
    if stat is None:
        raise HTTPException(status_code=404, detail="Stat not found")
    return stat


@stat_router.post("/stats/", response_model=StatResponse, tags=["Stats"])
def create_stat_route(
    stat_data: CreateStatRequest,
    stat_repo=Depends(get_stat_repository),
    stat_type_repo=Depends(get_stat_type_repository),
):
    try:
        stat = create_stat(stat_repo, stat_type_repo, stat_data.model_dump())
        return stat
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@stat_router.delete("/stats/{stat_id}", response_model=dict, tags=["Stats"])
def delete_stat_route(stat_id: int, repo=Depends(get_stat_repository)):
    stat = repo.get(stat_id)
    if stat is None:
        raise HTTPException(status_code=404, detail="Stat not found")
    delete_stat_by_id(repo, stat_id)
    return {"detail": "Stat deleted successfully"}

# calistats/interface/routes/stat_type_routes.py
"""
This file defines the API routes for managing StatType entities.
It provides endpoints for creating, retrieving, listing, and deleting stat types.
"""

from typing import List
from calistats.application.stat_type_use_cases import create_stat_type, get_stat_type_by_id, delete_stat_type_by_id
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from calistats.interface.dependencies import get_stat_type_repository

stat_type_router = APIRouter()


class CreateStatTypeRequest(BaseModel):
    name: str
    unit: str

    class Config:
        orm_mode = True


class StatTypeResponse(BaseModel):
    id: int
    name: str
    unit: str


@stat_type_router.get("/stat-types/", response_model=List[StatTypeResponse], tags=["Stat Types"])
def get_all_stat_types_route(repo=Depends(get_stat_type_repository)):
    return repo.get_all()


@stat_type_router.get("/stat-types/{stat_type_id}/", response_model=StatTypeResponse, tags=["Stat Types"])
def get_stat_type_route(stat_type_id: int, repo=Depends(get_stat_type_repository)):
    stat_type = get_stat_type_by_id(repo, stat_type_id)
    if stat_type is None:
        raise HTTPException(status_code=404, detail="Stat type not found")
    return stat_type


@stat_type_router.post("/stat-types/", response_model=StatTypeResponse, tags=["Stat Types"])
def create_stat_type_route(stat_type_data: CreateStatTypeRequest, repo=Depends(get_stat_type_repository)):
    stat_type = create_stat_type(repo, stat_type_data.model_dump())
    return stat_type


@stat_type_router.delete("/stat-types/{stat_type_id}", status_code=204, tags=["Stat Types"])
def delete_stat_type_route(stat_type_id: int, repo=Depends(get_stat_type_repository)):
    stat_type = repo.get(stat_type_id)
    if stat_type is None:
        raise HTTPException(status_code=404, detail="Stat type not found")
    delete_stat_type_by_id(repo, stat_type_id)
    return

# calistats/interface/routes/user_routes.py
"""
This file defines the API routes for managing User entities.
It provides endpoints for creating, retrieving, and deleting users.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from calistats.application.user_use_cases import create_user, get_user_by_email, get_user_by_id, delete_user_by_id
from calistats.interface.dependencies import get_user_repository

user_router = APIRouter()


class CreateUserRequest(BaseModel):
    email: str
    password: str
    name: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str


@user_router.get("/users/", response_model=list[UserResponse], tags=["Users"])
def get_all_users_route(repo=Depends(get_user_repository)):
    return repo.get_all()


@user_router.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user_route(user_id: int, repo=Depends(get_user_repository)):
    user = get_user_by_id(repo, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("/users/email/{email}", response_model=UserResponse, tags=["Users"])
def get_user_by_email_route(email: str, repo=Depends(get_user_repository)):
    user = get_user_by_email(repo, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post("/users/", response_model=UserResponse, tags=["Users"])
def create_user_route(
    user_data: CreateUserRequest,
    repo=Depends(get_user_repository),
):
    user = create_user(repo, user_data.model_dump())
    return user


@user_router.delete("/users/{user_id}", status_code=204, tags=["Users"])
def delete_user_route(user_id: int, repo=Depends(get_user_repository)):
    user = repo.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user_by_id(repo, user_id)
    return None

# calistats/main.py
"""
This is the main entry point for the FastAPI application.
It sets up the application and includes all routers to start the API server.
"""

from calistats.interface.main_router import main_router
from fastapi import FastAPI


app = FastAPI()

app.include_router(main_router)

# calistats.egg-info/dependency_links.txt


# calistats.egg-info/PKG-INFO
Metadata-Version: 2.1
Name: calistats
Version: 0.1.0
Summary: Calisthenics progress tracker
Home-page: UNKNOWN
Author: Amir Aharon
Author-email: amir.the.junior@gmail.com
License: UNKNOWN
Platform: UNKNOWN

UNKNOWN


# calistats.egg-info/requires.txt
fastapi
pydantic
pydantic[email]
pytest
python-dotenv
supabase
uvicorn

# calistats.egg-info/SOURCES.txt
setup.py
calistats.egg-info/PKG-INFO
calistats.egg-info/SOURCES.txt
calistats.egg-info/dependency_links.txt
calistats.egg-info/requires.txt
calistats.egg-info/top_level.txt
# calistats.egg-info/top_level.txt


# requirements.txt
fastapi
uvicorn
pydantic
pydantic[email]
pytest
python-dotenv
supabase
# setup.py
from setuptools import setup, find_packages


def fetch_requirements(filename="requirements.txt"):
    with open(filename, "r") as file:
        return file.read().splitlines()


setup(
    name="calistats",
    version="0.1.0",
    description="Calisthenics progress tracker",
    author="Amir Aharon",
    author_email="amir.the.junior@gmail.com",
    packages=find_packages(),
    install_requires=fetch_requirements(),
)

# structure.txt
.
├── calistats
│   ├── application
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── services.cpython-310.pyc
│   │   │   └── use_cases.cpython-310.pyc
│   │   └── use_cases.py
│   ├── domain
│   │   ├── models.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── models.cpython-310.pyc
│   │   │   └── repositories.cpython-310.pyc
│   │   └── repositories.py
│   ├── infrastructure
│   │   ├── file
│   │   │   ├── base_repository.py
│   │   │   ├── consts.py
│   │   │   ├── database.py
│   │   │   ├── __pycache__
│   │   │   │   ├── base_repository.cpython-310.pyc
│   │   │   │   ├── consts.cpython-310.pyc
│   │   │   │   ├── database.cpython-310.pyc
│   │   │   │   ├── repositories.cpython-310.pyc
│   │   │   │   └── utils.cpython-310.pyc
│   │   │   ├── repositories.py
│   │   │   ├── stats.json
│   │   │   └── stat_types.json
│   │   └── __pycache__
│   │       ├── database.cpython-310.pyc
│   │       ├── __init__.cpython-310.pyc
│   │       └── repositories.cpython-310.pyc
│   ├── interface
│   │   ├── dependencies.py
│   │   ├── main_router.py
│   │   ├── __pycache__
│   │   │   ├── dependencies.cpython-310.pyc
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── main_router.cpython-310.pyc
│   │   │   └── routes.cpython-310.pyc
│   │   └── routes
│   │       ├── __pycache__
│   │       │   ├── stat_routes.cpython-310.pyc
│   │       │   └── stat_type_routes.cpython-310.pyc
│   │       ├── stat_routes.py
│   │       └── stat_type_routes.py
│   ├── main.py
│   └── __pycache__
│       └── main.cpython-310.pyc
├── calistats.egg-info
│   ├── dependency_links.txt
│   ├── PKG-INFO
│   ├── requires.txt
│   ├── SOURCES.txt
│   └── top_level.txt
├── requirements.txt
├── setup.py
└── structure.txt
# tests/use_cases/test_stat_type_use_cases.py
import pytest
from unittest.mock import Mock
from calistats.domain.models import StatType
from calistats.application.stat_type_use_cases import create_stat_type, get_stat_type_by_id, delete_stat_type_by_id


@pytest.fixture
def stat_type_repo_mock():
    return Mock()


@pytest.fixture
def stat_type_data():
    return {"name": "Strength", "unit": "kg"}


@pytest.fixture
def stat_type():
    return StatType(id=1, name="Strength", unit="kg")


def test_create_stat_type(stat_type_repo_mock, stat_type_data):
    # Arrange
    stat_type_repo_mock.add = Mock()

    # Act
    result_stat_type = create_stat_type(stat_type_repo_mock, stat_type_data)

    # Assert
    assert result_stat_type.name == stat_type_data["name"]
    assert result_stat_type.unit == stat_type_data["unit"]
    stat_type_repo_mock.add.assert_called_once()


def test_get_stat_type_by_id(stat_type_repo_mock, stat_type):
    # Arrange
    stat_type_repo_mock.get.return_value = stat_type

    # Act
    result_stat_type = get_stat_type_by_id(stat_type_repo_mock, 1)

    # Assert
    assert result_stat_type.id == stat_type.id
    assert result_stat_type.name == stat_type.name
    assert result_stat_type.unit == stat_type.unit


def test_delete_stat_type_by_id(stat_type_repo_mock):
    # Arrange
    stat_type_repo_mock.get.return_value = Mock()  # Mock existing stat type
    stat_type_repo_mock.delete = Mock()

    # Act
    delete_stat_type_by_id(stat_type_repo_mock, 1)

    # Assert
    stat_type_repo_mock.delete.assert_called_once_with(1)

# tests/use_cases/test_stat_use_cases.py
import pytest
from unittest.mock import Mock
from calistats.domain.models import Stat
from calistats.application.stat_use_cases import create_stat, get_stat_by_id, delete_stat_by_id


@pytest.fixture
def stat_repo_mock():
    return Mock()


@pytest.fixture
def stat_type_repo_mock():
    return Mock()


@pytest.fixture
def stat_data():
    return {"user_id": 1, "stat_type_id": 1, "value": 100.0, "date": None}  # Allow it to be auto-generated in the test


@pytest.fixture
def stat():
    return Stat(id=1, user_id=1, stat_type_id=1, value=100.0, date="2024-08-14T00:00:00")


def assert_stat_equal(stat1: Stat, stat2: Stat):
    """Utility function to compare two Stat objects, ignoring 'id' field."""
    assert stat1.user_id == stat2.user_id
    assert stat1.stat_type_id == stat2.stat_type_id
    assert stat1.value == stat2.value
    assert stat1.date == stat2.date


def test_create_stat(stat_repo_mock, stat_type_repo_mock, stat_data):
    # Arrange
    stat_repo_mock.add = Mock()
    stat_type_repo_mock.get.return_value = Mock(id=1)

    # Act
    result_stat = create_stat(stat_repo_mock, stat_type_repo_mock, stat_data)

    # Assert
    assert_stat_equal(result_stat, Stat(id=result_stat.id, **stat_data))
    stat_repo_mock.add.assert_called_once()


def test_get_stat_by_id(stat_repo_mock, stat):
    # Arrange
    stat_repo_mock.get.return_value = stat

    # Act
    result_stat = get_stat_by_id(stat_repo_mock, 1)

    # Assert
    assert_stat_equal(result_stat, stat)


def test_delete_stat_by_id(stat_repo_mock):
    # Arrange
    stat_repo_mock.get.return_value = Mock()  # Mock existing stat
    stat_repo_mock.delete = Mock()

    # Act
    delete_stat_by_id(stat_repo_mock, 1)

    # Assert
    stat_repo_mock.delete.assert_called_once_with(1)

# tests/use_cases/test_user_use_cases.py
import pytest
from unittest.mock import Mock
from calistats.domain.models import User
from calistats.application.user_use_cases import create_user, get_user_by_id, get_user_by_email, delete_user_by_id


@pytest.fixture
def user_repo_mock():
    return Mock()


@pytest.fixture
def user_data():
    return {"name": "John Doe", "email": "john.doe@example.com", "password": "securepassword"}


@pytest.fixture
def user():
    return User(id=1, name="John Doe", email="john.doe@example.com", password="securepassword")


def test_create_user(user_repo_mock, user_data):
    # Arrange
    user_repo_mock.add = Mock()

    # Act
    result_user = create_user(user_repo_mock, user_data)

    # Assert
    assert result_user.name == user_data["name"]
    assert result_user.email == user_data["email"]
    assert result_user.password == user_data["password"]
    user_repo_mock.add.assert_called_once()


def test_get_user_by_id(user_repo_mock, user):
    # Arrange
    user_repo_mock.get.return_value = user

    # Act
    result_user = get_user_by_id(user_repo_mock, 1)

    # Assert
    assert result_user.id == user.id
    assert result_user.name == user.name
    assert result_user.email == user.email
    assert result_user.password == user.password


def test_get_user_by_email(user_repo_mock, user):
    # Arrange
    user_repo_mock.get_by_email.return_value = user

    # Act
    result_user = get_user_by_email(user_repo_mock, "john.doe@example.com")

    # Assert
    assert result_user.id == user.id
    assert result_user.name == user.name
    assert result_user.email == user.email
    assert result_user.password == user.password


def test_delete_user_by_id(user_repo_mock):
    # Arrange
    user_repo_mock.get.return_value = Mock()  # Mock existing user
    user_repo_mock.delete = Mock()

    # Act
    delete_user_by_id(user_repo_mock, 1)

    # Assert
    user_repo_mock.delete.assert_called_once_with(1)

# tests/utils.py
from typing import TypeVar


T = TypeVar("T")


def soft_compare(obj1: T, obj2: T, exclude: str = "id") -> bool:
    """Compare objects of the same type, ignoring the 'id' attribute"""
    if type(obj1) is not type(obj2):
        return False

    obj1_attrs = vars(obj1)
    obj2_attrs = vars(obj2)

    for key in obj1_attrs:
        if key != exclude:
            if obj1_attrs[key] != obj2_attrs.get(key):
                return False
    return True

