from google.adk.tools import ToolContext

from app.services.customer_service import get_customer_profile_data


def get_customer_profile(
    customer_id: str,
    tool_context: ToolContext,
) -> dict:
    """
    Retrieve a bank customer profile using the customer ID.

    Use this tool whenever the user asks to load a customer
    or requests customer-specific information.

    When a customer is successfully retrieved, make that customer
    the active customer for the current session.

    Args:
        customer_id: Customer identifier such as C123.

    Returns:
        Customer profile if found, otherwise an error response.
    """

    result = get_customer_profile_data(customer_id)

    if result["status"] != "success":
        return result

    customer = result["customer"]

    tool_context.state["active_customer_id"] = customer["customer_id"]
    tool_context.state["active_customer_name"] = customer["name"]

    return {
        **result,
        "session_context": {
            "active_customer_id": customer["customer_id"],
            "active_customer_name": customer["name"],
        },
    }