from pprint import pprint

from agents_flow_example.ollama_client import get_client_func
from pydantic import BaseModel, Field


class OrderScheme(BaseModel):
    """
     Scheme of order.
    Args:
        id:int - number from database
        name:str - is just name order
        place:str - is a place where order was created
        task_id:int - that's place in order
    """

    id: int = Field(description="id:int - number from database")
    name: str = Field(description="name:str - is just name order")
    place: str = Field(description="place:str - is a place where order was created")
    task_id: int = Field(description="task_id:int - that's place in order")


if __name__ == "__main__":
    model = get_client_func()
    model_with_structured_output = model.with_structured_output(OrderScheme)

    # resp = model_with_tools.invoke("summirize 2 and 6 and tell me answer")
    resp = model_with_structured_output.invoke(
        "order id 2, name pizza, was created in pizzaHut, task_id 30"
    )
    pprint(resp)
