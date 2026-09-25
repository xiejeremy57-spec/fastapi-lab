import asyncio
from llm import get_llm


async def main():
    llm = get_llm()
    response = await llm.ainvoke("你好，用一句话介绍自己")
    print(response.content)


if __name__ == "__main__":
    asyncio.run(main())