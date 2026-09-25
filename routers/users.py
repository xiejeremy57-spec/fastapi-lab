from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import User
from schemas import UserCreate, UserResponse
from service import user_service

router = APIRouter(
    prefix="/users",
    tags=["用户管理"]
)


@router.get("", response_model=list[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db)
):
    return user_service.get_users(db)
@router.post(
    "",
    response_model=UserResponse,
    status_code=201
)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return user_service.create_users(data,db)

@router.get("/search",response_model=UserResponse)
async def search_user(username:str,db:AsyncSession = Depends(get_db)):

    return await user_service.search_user(username,db)
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.update_user(user_id,data,db)
@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.delete_user(user_id,db)
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):


    return await user_service.get_user(user_id,db)
