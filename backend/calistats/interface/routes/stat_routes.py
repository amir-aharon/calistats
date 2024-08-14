"""
This file defines the API routes for managing Stat entities.
It provides endpoints for creating, retrieving, listing, and deleting stats.
"""

from calistats.application.stat_use_cases import create_stat, get_stat_by_id, delete_stat_by_id
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from calistats.interface.dependencies import get_stat_repository, get_stat_type_repository
from calistats.domain.models import Stat

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


@stat_router.get("/stats/", response_model=list[StatResponse])
def get_all_stats_route(repo=Depends(get_stat_repository)):
    return repo.get_all()


@stat_router.get("/stats/{stat_id}", response_model=StatResponse)
def get_stat_route(stat_id: int, repo=Depends(get_stat_repository)):
    stat = get_stat_by_id(repo, stat_id)
    if stat is None:
        raise HTTPException(status_code=404, detail="Stat not found")
    return stat


@stat_router.post("/stats/", response_model=StatResponse)
def create_stat_route(
    stat_data: CreateStatRequest,
    stat_repo=Depends(get_stat_repository),
    stat_type_repo=Depends(get_stat_type_repository),
):
    try:
        stat = create_stat(stat_repo, stat_type_repo, stat_data.dict())
        return stat
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@stat_router.delete("/stats/{stat_id}", response_model=dict)
def delete_stat_route(stat_id: int, repo=Depends(get_stat_repository)):
    stat = repo.get(stat_id)
    if stat is None:
        raise HTTPException(status_code=404, detail="Stat not found")
    delete_stat_by_id(repo, stat_id)
    return {"detail": "Stat deleted successfully"}
