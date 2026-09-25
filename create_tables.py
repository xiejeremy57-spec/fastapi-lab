import asyncio

from database import Base, engine
from models import User


async def main():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())