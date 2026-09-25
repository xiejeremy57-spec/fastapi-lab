from langchain_core.tools import tool

from database import AsyncSessionLocal
from schemas import UserResponse
from service import user_service
from pydantic import BaseModel, Field

class GetUserInput(BaseModel):
    user_id: int = Field(gt=0, description="要查询的用户 ID，必须大于 0")
@tool
async def list_users() -> dict:
    """查询数据库中的所有用户信息。"""

    async with AsyncSessionLocal() as db:

        users = await user_service.get_users(db)

        return {
            "users": [
                UserResponse.model_validate(user).model_dump(mode="json")
                for user in users
            ]
        }
@tool(args_schema=GetUserInput)
async def get_user_by_id(user_id: int) -> dict:
    """根据用户 ID 查询用户信息。"""

    async with AsyncSessionLocal() as db:

        user = await user_service.get_user(user_id,db)

        if user is None:
            return {
                "found": False,
                "message": "用户不存在"
            }

        return {
            "found": True,
            "user": UserResponse.model_validate(user).model_dump(mode="json")
        }