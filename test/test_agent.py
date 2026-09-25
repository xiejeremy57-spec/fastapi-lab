import asyncio

from langchain.agents import create_agent

from database import engine
from llm import get_llm
from agent_tool.user_tool import READ_TOOLS


async def main():
    llm = get_llm()

    agent = create_agent(
        model=llm,
        tools=READ_TOOLS,
        system_prompt="你是用户管理助手。查询用户信息时必须使用工具，不要编造数据。",
    )
   # 2. 调用 Agent
    try:
        result = await agent.ainvoke({
            "messages": [
                {"role": "user", "content": "查询 ID 为 1 的用户"}
            ]
        })

        print(result["messages"][-1].content)

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())