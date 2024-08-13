from calistats.infrastructure.file.repositories import (
    FileStatRepository,
    FileStatTypeRepository
)


def get_stat_repository() -> FileStatRepository:
    return FileStatRepository()


def get_stat_type_repository() -> FileStatTypeRepository:
    return FileStatTypeRepository()
