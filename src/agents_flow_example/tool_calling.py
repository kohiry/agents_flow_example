from pprint import pprint

from langchain.tools import tool
from agents_flow_example.ollama_client import get_client_func


@tool
def sum_2_digit(a: int, b: int):
    """
    Add 2 numbers
    """
    return f"Answer was: {a + b}"


if __name__ == "__main__":
    model = get_client_func()
    model_with_tools = model.bind_tools([sum_2_digit])

    # resp = model_with_tools.invoke("summirize 2 and 6 and tell me answer")
    resp = model_with_tools.invoke("20 and 12313")
    print(resp.tool_calls)
    if resp.tool_calls[0]["name"] == "sum_2_digit":
        resp = sum_2_digit.invoke(resp.tool_calls[0]["args"])

        pprint(resp)
