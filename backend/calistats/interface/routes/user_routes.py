"""
This file defines the API routes for managing User entities.
It provides endpoints for creating, retrieving, and deleting users.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from calistats.application.user_use_cases import create_user, get_user_by_email, get_user_by_id, delete_user_by_id
from calistats.interface.dependencies import get_user_repository

user_router = APIRouter()


class CreateUserRequest(BaseModel):
    email: str
    password: str
    name: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str


@user_router.get("/users/", response_model=list[UserResponse], tags=["Users"])
def get_all_users_route(repo=Depends(get_user_repository)):
    return repo.get_all()


@user_router.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user_route(user_id: int, repo=Depends(get_user_repository)):
    user = get_user_by_id(repo, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("/users/email/{email}", response_model=UserResponse, tags=["Users"])
def get_user_by_email_route(email: str, repo=Depends(get_user_repository)):
    user = get_user_by_email(repo, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post("/users/", response_model=UserResponse, tags=["Users"])
def create_user_route(
    user_data: CreateUserRequest,
    repo=Depends(get_user_repository),
):
    user = create_user(repo, user_data.model_dump())
    return user


@user_router.delete("/users/{user_id}", status_code=204, tags=["Users"])
def delete_user_route(user_id: int, repo=Depends(get_user_repository)):
    user = repo.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user_by_id(repo, user_id)
    return None
