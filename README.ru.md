# agents_flow_example

[English](README.md) | **Русский**

Небольшие самостоятельные примеры паттернов LLM-агентов на LangChain, LangGraph и MCP.
Всё работает локально на маленькой модели Ollama (`qwen3:0.6b-q4_K_M`), API-ключи не нужны.

## Быстрый старт

Нужны: [uv](https://docs.astral.sh/uv/) и [Ollama](https://ollama.com/).

```bash
# 1. Запустить Ollama (пропустите, если она уже работает как сервис) и скачать модель
ollama serve &
ollama pull qwen3:0.6b-q4_K_M

# 2. Установить зависимости (uv сам скачает Python 3.13, если его нет)
uv sync

# 3. Посмотреть список примеров и запустить один
uv run agents-flow-example
uv run agents-flow-example mcp
```

Запускайте команды из корня репозитория: пример RAG хранит векторную БД в `./.vector_db`.

## Примеры

| Имя | Модуль | Что показывает |
|---|---|---|
| `chain` | `ollama_client.py` | Шаблон промпта, переданный в LLM (`prompt \| model`) |
| `tools` | `tool_calling.py` | `bind_tools`: модель выбирает инструмент, скрипт его вызывает |
| `structured` | `structured_output.py` | `with_structured_output`: свободный текст разбирается в pydantic-модель |
| `search` | `search_loop.py` | Генерация поисковых запросов, поиск в DuckDuckGo, оценка каждого результата, ответ по полезным |
| `rag` | `rag.py` | RAG на LangGraph поверх Chroma: поиск, оценка документов, переписывание запроса и повтор, затем ответ |
| `mcp` | `mcp_clients/ai_using_mcp.py` | Агент на LangGraph, вызывающий инструменты MCP-сервера (`mcp_clients/mcp_client.py`) через stdio |

Каждый модуль можно запустить и напрямую:

```bash
uv run python -m agents_flow_example.rag
uv run python -m agents_flow_example.mcp_clients.ai_using_mcp
```

MCP-сервер заказов можно запустить отдельно (транспорт stdio), например чтобы подключить его к другому MCP-клиенту:

```bash
uv run python src/agents_flow_example/mcp_clients/mcp_client.py
```

## Структура проекта

```
src/agents_flow_example/
├── __init__.py            # лаунчер `agents-flow-example`
├── ollama_client.py       # общая фабрика модели (модель меняется здесь)
├── tool_calling.py
├── structured_output.py
├── search_loop.py         # нужен доступ в интернет
├── rag.py                 # при первом запуске скачивает all-MiniLM-L6-v2
└── mcp_clients/
    ├── mcp_client.py      # MCP-сервер: заказы в памяти с CRUD-инструментами
    └── ai_using_mcp.py    # агент, который использует эти инструменты
```

## Заметки

- **Смена модели.** Правьте `ollama_client.py`. Модель на 0.6B быстрая, но ненадёжно вызывает инструменты:
  `tools` иногда не получает вызова инструмента и падает, а агент может вообще не использовать инструменты.
  `qwen3:4b` и крупнее работают заметно лучше.
- **Имена инструментов важны.** Маленькие модели выбирают инструмент, сопоставляя имя, описание и имена
  аргументов с запросом, поэтому `get_order(order_id)` срабатывает там, где `order_by_id(id)` не срабатывал.
- **`mcp` закреплён на 1.x**, потому что `langchain-mcp-adapters` пока не поддерживает `mcp` 2.x.
- `Connection refused` от `httpx` означает, что Ollama не запущена.
