import json
from pathlib import Path


CUSTOMER_FILE = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "customers"
    / "customers.json"
)


def get_customer_profile_data(customer_id: str) -> dict:
    """
    Retrieve customer profile data from the customer data source.

    This function contains the core customer lookup logic.
    It is independent of ADK and MCP.
    """

    with open(CUSTOMER_FILE, "r", encoding="utf-8") as file:
        customers = json.load(file)

    customer_id = customer_id.upper()
    customer = customers.get(customer_id)

    if not customer:
        return {
            "status": "not_found",
            "message": f"No customer found for ID {customer_id}",
        }

    return {
        "status": "success",
        "customer": customer,
    }