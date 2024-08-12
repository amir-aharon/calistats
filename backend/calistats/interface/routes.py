from calistats.application.use_cases import create_stat
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from calistats.interface.dependencies import get_stat_repository

router = APIRouter()


class CreateStatRequest(BaseModel):
    name: str
    owner: int
    unit: str
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
    print(stat_data.model_dump())
    stat = create_stat(repo, stat_data.model_dump())
    return stat
