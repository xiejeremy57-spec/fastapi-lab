from langchain.tools import tool
from pydantic import BaseModel, Field
from fastapi import HTTPException

from database import AsyncSessionLocal
from service import user_service
from schemas import UserCreate, UserResponse


# ---------- 公共方法：ORM 转换为字典 ----------

def to_user_dict(user) -> dict:
    return UserResponse.model_validate(user).model_dump(mode="json")


# ---------- 工具参数定义 ----------

class GetUserInput(BaseModel):
    user_id: int = Field(gt=0, description="要查询的用户 ID，必须大于 0")


class DeleteUserInput(BaseModel):
    user_id: int = Field(gt=0, description="要删除的用户 ID，必须大于 0")


class UpdateUserInput(UserCreate):
    user_id: int = Field(gt=0, description="要修改的用户 ID，必须大于 0")


# ---------- 1. 查询全部用户 ----------

@tool
async def list_users() -> dict:
    """查询数据库中的所有用户信息。"""

    async with AsyncSessionLocal() as db:
        users = await user_service.get_users(db)

        return {
            "users": [to_user_dict(user) for user in users]
        }


# ---------- 2. 根据 ID 查询用户 ----------

@tool(args_schema=GetUserInput)
async def get_user_by_id(user_id: int) -> dict:
    """根据用户 ID 查询用户详细信息。"""

    async with AsyncSessionLocal() as db:
        try:
            # 这里使用你已经验证过的参数顺序
            user = await user_service.get_user(user_id=user_id, db=db)

            if user is None:
                return {
                    "found": False,
                    "message": "用户不存在"
                }

            return {
                "found": True,
                "user": to_user_dict(user)
            }

        except HTTPException as e:
            if e.status_code == 404:
                return {
                    "found": False,
                    "message": "用户不存在"
                }
            raise


# ---------- 3. 新增用户 ----------

@tool(args_schema=UserCreate)
async def create_user(**kwargs) -> dict:
    """创建一个新用户。"""

    user_data = UserCreate.model_validate(kwargs)

    async with AsyncSessionLocal() as db:
        # 按你的 Service 实际参数顺序调整这一行
        user = await user_service.create_user(user_data, db)

        return {
            "success": True,
            "user": to_user_dict(user)
        }


# ---------- 4. 修改用户 ----------

@tool(args_schema=UpdateUserInput)
async def update_user(**kwargs) -> dict:
    """根据用户 ID 修改用户信息。"""

    user_id = kwargs.pop("user_id")
    user_data = UserCreate.model_validate(kwargs)

    async with AsyncSessionLocal() as db:
        try:
            # 按你的 Service 实际参数顺序调整这一行
            user = await user_service.update_user(user_id, user_data, db)

            if user is None:
                return {
                    "success": False,
                    "message": "用户不存在"
                }

            return {
                "success": True,
                "user": to_user_dict(user)
            }

        except HTTPException as e:
            if e.status_code == 404:
                return {
                    "success": False,
                    "message": "用户不存在"
                }
            raise


# ---------- 5. 删除用户 ----------

@tool(args_schema=DeleteUserInput)
async def delete_user(user_id: int) -> dict:
    """根据用户 ID 删除用户。"""

    async with AsyncSessionLocal() as db:
        try:
            # 按你的 Service 实际参数顺序调整这一行
            await user_service.delete_user(user_id, db)

            return {
                "success": True,
                "message": f"用户 {user_id} 已删除"
            }

        except HTTPException as e:
            if e.status_code == 404:
                return {
                    "success": False,
                    "message": "用户不存在"
                }
            raise


# ---------- 工具集合 ----------

# 默认提供给 AI 的只读工具
READ_TOOLS = [
    list_users,
    get_user_by_id,
]

# 涉及数据库写入的工具，先单独放着
WRITE_TOOLS = [
    create_user,
    update_user,
    delete_user,
]