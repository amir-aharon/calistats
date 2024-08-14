"""
This file defines the API routes for managing Stat entities.
It provides endpoints for creating, retrieving, and listing stats.
"""

from calistats.application.use_cases import create_stat
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from calistats.interface.dependencies import get_stat_repository, get_stat_type_repository

stat_router = APIRouter()


class CreateStatRequest(BaseModel):
    owner_id: int
    stat_type_id: int
    value: float


@stat_router.get("/stats/")
def get_all_stats_route(repo=Depends(get_stat_repository)):
    return repo.get_all()


@stat_router.post("/stats/")
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


@stat_router.delete("/stats/{stat_id}")
def delete_stat_route(stat_id: int, repo=Depends(get_stat_repository)):
    stat = repo.get(stat_id)
    if stat is None:
        return {"detail": "Stat not found"}
    repo.delete(stat_id)
    return {"detail": "Stat deleted successfully"}
