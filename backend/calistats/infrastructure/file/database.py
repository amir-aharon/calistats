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
