import runpy
import sys

EXAMPLES = {
    "chain": ("ollama_client", "Prompt template + LLM chain"),
    "tools": ("tool_calling", "Model picks a tool and we call it"),
    "structured": ("structured_output", "Parse text into a pydantic model"),
    "search": ("search_loop", "Web search loop with usefulness grading"),
    "rag": ("rag", "LangGraph RAG over Chroma with grading and query rewrite"),
    "mcp": ("mcp_clients.ai_using_mcp", "LangGraph agent using MCP order server tools"),
}


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    if name not in EXAMPLES:
        print("Usage: uv run agents-flow-example <example>\n")
        for key, (_, description) in EXAMPLES.items():
            print(f"  {key:<11} {description}")
        sys.exit(0 if not name else 1)

    module, _ = EXAMPLES[name]
    runpy.run_module(f"agents_flow_example.{module}", run_name="__main__", alter_sys=True)
