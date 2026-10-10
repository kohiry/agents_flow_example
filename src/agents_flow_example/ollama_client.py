from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaLLM


def get_client() -> OllamaLLM:
    return OllamaLLM(model="qwen3:0.6b-q4_K_M")


def get_client_func() -> ChatOllama:
    return ChatOllama(model="qwen3:0.6b-q4_K_M")


if __name__ == "__main__":
    template = """
    Question: {question}

    Answer: let's think step by step.
    """

    prompt = ChatPromptTemplate.from_template(template)
    model = get_client()

    chain = prompt | model

    res = chain.invoke({"question": "What is Langchain?"})
    print(res)
