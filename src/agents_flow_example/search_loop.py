from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from agents_flow_example.ollama_client import get_client_func
from pydantic import BaseModel, Field

search = DuckDuckGoSearchRun(api_wrapper=DuckDuckGoSearchAPIWrapper(region="us-en"))


class SearchQuery(BaseModel):
    questions: list[str] = Field(description="list of questions for search, minimum 5 questions")


class Classificator(BaseModel):
    useful: bool = Field(description="True if Yes, False if No")


@tool
def sum_2_digit(a: int, b: int):
    """
    Add 2 numbers
    """
    return f"Answer was: {a + b}"


if __name__ == "__main__":
    model = get_client_func()

    m2 = model.with_structured_output(SearchQuery)
    m3 = model.with_structured_output(Classificator)

    # resp = model_with_tools.invoke("summirize 2 and 6 and tell me answer")
    request = "whats is the different with PostgreSQL, ChatGPT, Python"
    res_scheme: SearchQuery = m2.invoke(request)
    answer_of_questions = []
    print(res_scheme.questions)
    for q in res_scheme.questions:
        # answer_of_questions.append(search.invoke(q))
        s = search.invoke(q)
        r = m3.invoke(
            f"Question: {request}. Tell me was that search useful for answer? Yes or No. Search: {s}"
        )
        print(r)
        if r.useful:
            answer_of_questions.append(s)
    print(answer_of_questions)
    resp = model.invoke(f"Question: {request}. Additional info: {';'.join(answer_of_questions)}")
    print(resp.content)
