# agents_flow_example

**English** | [Русский](README.ru.md)

Small, self-contained examples of LLM agent patterns built with LangChain, LangGraph and MCP.
Everything runs locally on a small Ollama model (`qwen3:0.6b-q4_K_M`), so no API keys are needed.

## Quick start

Requirements: [uv](https://docs.astral.sh/uv/) and [Ollama](https://ollama.com/).

```bash
# 1. Start Ollama (skip if it already runs as a service) and pull the model
ollama serve &
ollama pull qwen3:0.6b-q4_K_M

# 2. Install dependencies (Python 3.13 is fetched by uv if missing)
uv sync

# 3. List the examples and run one
uv run agents-flow-example
uv run agents-flow-example mcp
```

Run commands from the repository root: the RAG example keeps its vector DB in `./.vector_db`.

## Examples

| Name | Module | What it shows |
|---|---|---|
| `chain` | `ollama_client.py` | Prompt template piped into the LLM (`prompt \| model`) |
| `tools` | `tool_calling.py` | `bind_tools`: the model chooses a tool and the script calls it |
| `structured` | `structured_output.py` | `with_structured_output`: free text parsed into a pydantic model |
| `search` | `search_loop.py` | Generate search queries, search DuckDuckGo, grade each result, answer with the useful ones |
| `rag` | `rag.py` | LangGraph RAG over Chroma: retrieve, grade documents, rewrite the query and retry, then answer |
| `mcp` | `mcp_clients/ai_using_mcp.py` | LangGraph agent that calls tools of an MCP server (`mcp_clients/mcp_client.py`) over stdio |

Each module can also be run directly:

```bash
uv run python -m agents_flow_example.rag
uv run python -m agents_flow_example.mcp_clients.ai_using_mcp
```

The MCP order server can be started on its own (stdio transport), e.g. to plug it into another MCP client:

```bash
uv run python src/agents_flow_example/mcp_clients/mcp_client.py
```

## Project layout

```
src/agents_flow_example/
├── __init__.py            # `agents-flow-example` launcher
├── ollama_client.py       # shared model factory (change the model here)
├── tool_calling.py
├── structured_output.py
├── search_loop.py         # needs internet access
├── rag.py                 # downloads all-MiniLM-L6-v2 on first run
└── mcp_clients/
    ├── mcp_client.py      # MCP server: in-memory orders with CRUD tools
    └── ai_using_mcp.py    # agent that uses those tools
```

## Notes

- **Changing the model.** Edit `ollama_client.py`. A 0.6B model is fast but unreliable at tool calling:
  `tools` sometimes returns no tool call and fails, and the agent may skip tools entirely.
  `qwen3:4b` or larger behaves much better.
- **Tool naming matters.** Small models choose tools by matching names, descriptions and argument
  names against the request, so `get_order(order_id)` works where `order_by_id(id)` did not.
- **`mcp` is pinned to 1.x** because `langchain-mcp-adapters` does not support `mcp` 2.x yet.
- `Connection refused` from `httpx` means Ollama is not running.
