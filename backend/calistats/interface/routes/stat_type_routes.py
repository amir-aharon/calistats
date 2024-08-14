"""
This file defines the API routes for managing StatType entities.
It provides endpoints for retrieving stat types by ID.
"""

from calistats.application.use_cases import create_stat_type, get_stat_type
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from calistats.interface.dependencies import get_stat_type_repository

stat_type_router = APIRouter()


class CreateStatTypeRequest(BaseModel):
    name: str
    unit: str


@stat_type_router.get("/stat-types/")
def get_all_stat_types_route(repo=Depends(get_stat_type_repository)):
    return repo.get_all()


@stat_type_router.get("/stat-types/{stat_type_id}/")
def get_stat_type_route(stat_type_id: int, repo=Depends(get_stat_type_repository)):
    stat_type = get_stat_type(repo, stat_type_id)
    if stat_type is None:
        raise HTTPException(status_code=404, detail="Stat type not found")
    return stat_type


@stat_type_router.post("/stat-types/")
def create_stat_type_route(stat_type_data: CreateStatTypeRequest, repo=Depends(get_stat_type_repository)):
    stat_type = create_stat_type(repo, stat_type_data.model_dump())
    return stat_type
