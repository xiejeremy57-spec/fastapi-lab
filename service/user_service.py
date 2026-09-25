from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas import UserCreate


async def get_users(db: AsyncSession):
    stmt = select(User)

    result = await db.execute(stmt)

    users = result.scalars().all()

    return users
async def create_users(data: UserCreate,db: AsyncSession):
    user = User(
        username=data.username,
        age=data.age,
        email=str(data.email)
    )

    db.add(user)

    await db.commit()

    await db.refresh(user)

    return user
async def search_user(username:str,db:AsyncSession ):
    # 1. 构建带 where 条件的查询语句
    stmt = select(User).where(User.username == username)
    # 2. 执行查询
    result = await db.execute(stmt)
    # 3. 获取单条查询结果
    user = result.scalar_one_or_none()

    # 4. 判断用户是否存在，不存在则抛出 404
    if user is None:
        raise HTTPException(status_code=404, detail="找不到")
    # 5. 返回用户
    return user
async def update_user(
    user_id: int,
    data: UserCreate,
    db: AsyncSession
):
    # 1. 根据 ID 查询用户
    result =await db.get(User,user_id)

    # 2. 判断用户是否存在，不存在返回 404
    if result is None:
        raise HTTPException(status_code=404,detail="用户不存在")
    # 3. 修改 username、age、email
    result.username=data.username
    result.age=data.age
    result.email=data.email
    # 4. 提交事务
    await db.commit()
    # 5. 返回修改后的用户
    return result
async def delete_user(
    user_id: int,
    db: AsyncSession
):
    # 1. 根据 ID 查询用户
    result = await db.get(User,user_id)

    # 2. 如果用户不存在，返回 404
    if result is None:
        raise HTTPException(status_code=404,detail="用户不存在")
    # 3. 删除用户
    await db.delete(result)
    await db.commit()
    # 4. 提交事务
async def get_user(
    user_id: int,
    db: AsyncSession
):
    user = await db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )

    return user