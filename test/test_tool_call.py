import asyncio

from llm import get_llm
from agent_tool.user_tool import READ_TOOLS


async def main():
    llm = get_llm()

    # 把工具提供给模型
    llm_with_tools = llm.bind_tools(READ_TOOLS)

    response = await llm_with_tools.ainvoke(
        "帮我查询 ID 为 1 的用户信息"
    )

    print("模型回复：", response.content)
    print("工具调用：", response.tool_calls)


if __name__ == "__main__":
    asyncio.run(main())