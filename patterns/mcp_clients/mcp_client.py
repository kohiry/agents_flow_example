from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Order Server")

ORDERS = [
    {"id": 1, "item": "Keyboard", "status": "shipped"},
    {"id": 2, "item": "Mouse", "status": "processing"},
    {"id": 3, "item": "Monitor", "status": "delivered"},
]


@mcp.tool()
def list_orders() -> list[dict]:
    """return all availible orders"""
    return ORDERS


@mcp.tool()
def get_order(order_id: int) -> dict:
    """Get an order by its ID."""
    for order in ORDERS:
        if order["id"] == order_id:
            return order

    return {"error": f"Order {order_id} not found"}


@mcp.tool()
def add_order(order: dict) -> int:
    """Add order"""
    ORDERS.append(order)
    return 200


@mcp.tool()
def del_order(id: int) -> int:
    """Delete Order by {id}"""

    for i, order in enumerate(ORDERS):
        if order["id"] == id:
            del ORDERS[i]
            break
    return 200


if __name__ == "__main__":
    mcp.run(transport="stdio")
