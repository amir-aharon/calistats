from fastapi import APIRouter
from calistats.application.services import get_message

router = APIRouter()


@router.get("/msg")
def read_item():
    return get_message()
