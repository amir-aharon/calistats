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
    try:
        stat_type = create_stat_type(repo, stat_type_data.model_dump())
        return stat_type
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@stat_type_router.delete("/stat-types/{stat_type_id}", status_code=204, tags=["Stat Types"])
def delete_stat_type_route(stat_type_id: int, repo=Depends(get_stat_type_repository)):
    stat_type = repo.get(stat_type_id)
    if stat_type is None:
        raise HTTPException(status_code=404, detail="Stat type not found")
    delete_stat_type_by_id(repo, stat_type_id)
    return
