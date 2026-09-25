import asyncio

from agent_tool.user_tool import get_user_by_id
from database import engine


async def main():

    result = await get_user_by_id.ainvoke({
        "user_id": 1
    })

    print(result)
    print(get_user_by_id.args)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())