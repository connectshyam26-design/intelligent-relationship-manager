import asyncio

from mcp import Client
from mcp.types import TextContent

from mcp_server import mcp


async def main():
    async with Client(mcp) as client:

        tools = await client.list_tools()

        print("Available MCP tools:")
        for tool in tools.tools:
            print("-", tool.name)

        result = await client.call_tool(
            "get_customer_profile",
            {
                "customer_id": "C123",
            },
        )

        print("\nTool error status:")
        print(result.is_error)

        print("\nTool content:")

        for block in result.content:
            if isinstance(block, TextContent):
                print(block.text)

        print("\nStructured content:")
        print(result.structured_content)


if __name__ == "__main__":
    asyncio.run(main())