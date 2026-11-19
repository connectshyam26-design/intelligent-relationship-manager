from mcp.server import MCPServer

from app.services.customer_service import get_customer_profile_data


mcp = MCPServer("IRM MCP Server")


@mcp.tool()
def get_customer_profile(customer_id: str) -> dict:
    """
    Retrieve a bank customer profile using the customer ID.

    Args:
        customer_id: Customer identifier such as C123.

    Returns:
        Customer profile if found, otherwise an error response.
    """

    return get_customer_profile_data(customer_id)

if __name__ == "__main__":
    mcp.run()