import os
import sys

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from app.rag import search_product_policy
from app.rules import (
    check_eligibility,
    find_eligible_alternatives,
)

load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY is not configured")

# Absolute path to the MCP server
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MCP_SERVER_PATH = os.path.join(
    PROJECT_ROOT,
    "mcp_server.py",
)


customer_mcp_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[MCP_SERVER_PATH],
        )
    ),
    tool_filter=["get_customer_profile"],
)

def update_customer_session_state(
    tool,
    args: dict,
    tool_context: ToolContext,
    tool_response,
):
    """
    Update ADK session state after the MCP customer tool returns.
    """

    if getattr(tool, "name", None) != "get_customer_profile":
        return None

    if not isinstance(tool_response, dict):
        return None

    if tool_response.get("status") != "success":
        return None

    customer = tool_response.get("customer")

    if not customer:
        return None

    tool_context.state["active_customer_id"] = customer["customer_id"]
    tool_context.state["active_customer_name"] = customer["name"]

    return None

root_agent = Agent(
    name="irm_agent",
    model="gemini-flash-latest",
    instruction="""
    You are an Intelligent Relationship Manager assistant for a bank.
    
    Current active customer ID: {active_customer_id?}
    Current active customer name: {active_customer_name?}

    You assist relationship managers with customer information,
    product policies and product eligibility.

    Follow these rules carefully:

    1. CUSTOMER DATA
    For customer-specific information, always use
    get_customer_profile.
    Never invent customer information.
    

    2. PRODUCT POLICY
    For product eligibility criteria, features or policy questions,
    always use search_product_policy.
    Do not invent or rely on remembered product policy.

    3. ELIGIBILITY
    When asked whether a customer is eligible for a product:
    - retrieve the customer profile,
    - retrieve the relevant product policy,
    - use check_eligibility for the final deterministic decision.
    -When a customer is NOT ELIGIBLE for the requested product:
    - use find_eligible_alternatives,
    - recommend the most suitable eligible alternative,
    - clearly explain why the original product failed
    and why the alternative is suitable.

    4. Never independently decide hard eligibility rules when
    check_eligibility is available.

    5. Explain the eligibility result clearly using the tool outputs.

    6. If customer information, product policy or required information
    is unavailable, say so clearly.

    7. Never claim to have accessed data that was not returned by a tool.
    8. RESPONSE FORMAT FOR ELIGIBILITY QUESTIONS

    When responding to an eligibility question, always use this structure:

    Eligibility Result

    Customer: <customer_id> — <customer_name>
    Product: <product_name>
    Decision: ELIGIBLE or NOT ELIGIBLE

    Reason
    - Age: Pass/Fail
    - Annual Income: Pass/Fail
    - KYC Status: Pass/Fail
    - Risk Segment: Pass/Fail

    Recommendation
    <one concise recommendation sentence>

    Keep the response concise.
    Do not repeat full customer profile details unless they are directly relevant.
    Do not include long summaries.
    
    9. ALTERNATIVE PRODUCTS

    If a customer is NOT ELIGIBLE for the requested product:

    - Use find_eligible_alternatives.
    - Do not invent alternative products.
    - Recommend only products returned by the tool.
    - Clearly explain why the requested product failed.
    - Prefer the most suitable eligible alternative rather than simply listing all products.
    """,
    tools=[
        customer_mcp_tools,
        search_product_policy,
        check_eligibility,
        find_eligible_alternatives,
    ],
    
    after_tool_callback=update_customer_session_state,
)