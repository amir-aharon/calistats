from calistats.application.use_cases import create_stat, create_stat_type, get_stat_type
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from calistats.interface.dependencies import get_stat_repository, get_stat_type_repository

router = APIRouter()


class CreateStatRequest(BaseModel):
    owner_id: int
    stat_type_id: int
    value: float
    date: str


@router.get("/stats/")
def get_all_stats_route(repo=Depends(get_stat_repository)):
    return repo.get_all()


@router.post("/stats/")
def create_stat_route(
    stat_data: CreateStatRequest,
    repo=Depends(get_stat_repository)
):
    stat = create_stat(repo, stat_data.model_dump())
    return stat


class CreateStatTypeRequest(BaseModel):
    name: str
    unit: str


@router.get("/stat-types/")
def get_all_stat_types_route(repo=Depends(get_stat_type_repository)):
    return repo.get_all()


@router.get("/stat-types/{stat_type_id}/")
def get_stat_type_route(
    stat_type_id: int,
    repo=Depends(get_stat_type_repository)
):
    stat_type = get_stat_type(repo, stat_type_id)
    if stat_type is None:
        raise HTTPException(status_code=404, detail="Stat type not found")
    return stat_type


@router.post("/stat-types/")
def create_stat_type_route(
    stat_type_data: CreateStatTypeRequest,
    repo=Depends(get_stat_type_repository)
):
    stat_type = create_stat_type(repo, stat_type_data.model_dump())
    return stat_type
