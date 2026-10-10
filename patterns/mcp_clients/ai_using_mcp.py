import sys
from asyncio import run
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from ollama_client import get_client_func

BASE_DIR = Path(__file__).resolve().parent
SERVER_PATH = BASE_DIR / "mcp_client.py"


async def main():
    client = MultiServerMCPClient(
        {
            "orders": {
                "command": sys.executable,
                "args": [str(SERVER_PATH)],
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    m = get_client_func()
    m = m.bind_tools(tools)

    def call_model(state: MessagesState):
        response = m.invoke(state["messages"])
        return {"messages": [response]}

    builder = StateGraph(MessagesState)
    builder.add_node("agent", call_model)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    graph = builder.compile()
    result = await graph.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": ("Give me order  with id 2 and tell me his status"),
                }
            ]
        }
    )
    print("\n Final Answer")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    run(main())
