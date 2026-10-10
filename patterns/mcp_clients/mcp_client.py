from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Order Server")

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
def order_by_id(id: int) -> dict:
    """Return order by id"""
    for order in ORDERS:
        if order["id"] == id:
            return order


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
