from typing import TypedDict

import chromadb
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from ollama_client import get_client_func
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

client_rag = chromadb.PersistentClient(path=".vector_db")
model_embedder = SentenceTransformer("all-MiniLM-L6-v2")
model = get_client_func()
collection = client_rag.get_or_create_collection("documents")


class Classificator(BaseModel):
    useful: bool = Field(description="True if Yes, False if No")


m3 = model.with_structured_output(Classificator)


class RagState(TypedDict):
    question: str
    query: str
    documents: list[str]
    answer: str
    retries: int
    useful: bool


def search_rag(q):
    query_embeddings = model_embedder.encode([q]).tolist()
    results = collection.query(query_embeddings=query_embeddings, n_results=2)
    return results["documents"][0]


def retrieve(state: RagState):
    docs = search_rag(state["query"])

    return {"documents": docs}


def grade_documents(state: RagState):
    answer_of_questions = []
    for d in state["documents"]:
        r = m3.invoke(
            f"Question: {state['question']}. Tell me was that search useful for answer? "
            f"Yes or No. Search: {d}"
        )
        if r.useful:
            answer_of_questions.append(d)

    return {"documents": answer_of_questions, "useful": bool(answer_of_questions)}


def no_answer(state: RagState):
    return {"answer": "Not Find correct docs"}


def rewrite_query(state: RagState):
    return {
        "query": model.invoke(
            f"{state['question']}\nWrite a more specific question. Reply with the question only."
        ).content,
        "retries": state["retries"] + 1,
    }


def generate(state: RagState):
    answer = model.invoke(
        f"Questions: {state['question']}\nContext: {state['documents']}",
    )
    return {"answer": answer.content}


def route_after_grades(state):
    if state["useful"]:
        return "generate"
    if state["retries"] >= 2:
        return "no_answer"

    return "rewrite"


builder = StateGraph(RagState)
builder.add_node("retrieve", retrieve)
builder.add_node("grade", grade_documents)
builder.add_node("rewrite", rewrite_query)
builder.add_node("generate", generate)
builder.add_node("no_answer", no_answer)
builder.add_edge(
    START,
    "retrieve",
)
builder.add_edge(
    "retrieve",
    "grade",
)
builder.add_conditional_edges(
    "grade",
    route_after_grades,
    {
        "rewrite": "rewrite",
        "generate": "generate",
        "no_answer": "no_answer",
    },
)
builder.add_edge(
    "rewrite",
    "retrieve",
)
builder.add_edge(
    "generate",
    END,
)

builder.add_edge(
    "no_answer",
    END,
)

if __name__ == "__main__":
    q = [
        "PostgreSQL is an open-source relational database management system (RDBMS) used to store, manage, and query structured data using SQL.",
        "ChatGPT is an AI assistant developed by OpenAI that can answer questions, generate content, write code, analyze information, and help with problem-solving.",
        "Claude is an AI assistant developed by Anthropic that can understand and generate text, write code, analyze documents, and assist with reasoning and other tasks.",
        "Claude Code is an AI-powered coding tool developed by Anthropic that works in your terminal to understand codebases, edit files, run commands, debug issues, and help automate software development tasks.",
        "Codex is OpenAI's AI-powered coding agent that can write, review, debug, and modify code, as well as perform software development tasks in supported environments.",
    ]
    embeddings = model_embedder.encode(q).tolist()
    collection.upsert(
        ids=[str(i) for i in range(1, len(q) + 1)],
        documents=q,
        embeddings=embeddings,
    )
    graph = builder.compile()
    question = "What is a difference between Claude code and Postgres?"
    result = graph.invoke({"question": question, "query": question, "retries": 0})
    print(result)
