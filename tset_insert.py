import asyncio

from database import AsyncSessionLocal, engine
from models import User


async def main():

    # 创建 Session
    async with AsyncSessionLocal() as session:

        # 创建 ORM 对象
        user = User(
            username="zhangsan",
            age=20,
            email="zhangsan@example.com"
        )

        # 加入 Session
        session.add(user)

        # 提交事务
        await session.commit()

        # 从数据库刷新对象
        await session.refresh(user)

        print("插入成功！")
        print("用户 ID:", user.id)
        print("用户名:", user.username)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())