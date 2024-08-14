from calistats.application.use_cases import create_stat
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from calistats.interface.dependencies import get_stat_repository

stat_router = APIRouter()


class CreateStatRequest(BaseModel):
    owner_id: int
    stat_type_id: int
    value: float
    date: str


@stat_router.get("/stats/")
def get_all_stats_route(repo=Depends(get_stat_repository)):
    return repo.get_all()


@stat_router.post("/stats/")
def create_stat_route(
    stat_data: CreateStatRequest,
    repo=Depends(get_stat_repository)
):
    stat = create_stat(repo, stat_data.model_dump())
    return stat
