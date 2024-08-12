import json
from typing import List
from calistats.domain.models import Stat

JSON_FILE = 'calistats/infrastructure/stats.json'


def read_stats_from_file() -> List[Stat]:
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
        return [Stat(**item) for item in data]
    except FileNotFoundError as e:
        print(f"Error reading file: {e}")
    except json.JSONDecodeError:
        with open(JSON_FILE, 'w') as file:
            json.dump([], file)
    finally:
        return []


def write_stats_to_file(stats: List[Stat]) -> None:
    with open(JSON_FILE, 'w') as file:
        json.dump([stat.model_dump() for stat in stats], file)
