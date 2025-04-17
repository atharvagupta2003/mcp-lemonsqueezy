import os
import json
import logging
import aiohttp
from dotenv import load_dotenv
import mcp.server.stdio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent
from tools import get_lemonsqueezy_tools
from utils import get_auth_headers

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lemonsqueezy-mcp-server")

class LemonSqueezyManager:
    def __init__(self):
        self.base_url = "https://api.lemonsqueezy.com/v1"
        self.session = aiohttp.ClientSession()

    async def request(self, method, endpoint, params=None, json_data=None):
        url = f"{self.base_url}{endpoint}"
        headers = get_auth_headers()
        async with self.session.request(method, url, headers=headers, params=params, json=json_data) as response:
            if response.status >= 400:
                raise Exception(f"{response.status}: {await response.text()}")
            return await response.json()

    async def close(self):
        await self.session.close()

async def main():
    logger.info("Starting Lemon Squeezy MCP Server")

    ls = LemonSqueezyManager()
    server = Server("lemonsqueezy-mcp-server")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return get_lemonsqueezy_tools()

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            logger.info(f"Tool: {name}")
            if name == "get_user":
                data = await ls.request("GET", "/users/me")
            elif name == "list_stores":
                data = await ls.request("GET", "/stores")
            elif name == "get_store":
                data = await ls.request("GET", f"/stores/{arguments['store_id']}")
            elif name == "list_products":
                data = await ls.request("GET", "/products")
            elif name == "get_product":
                data = await ls.request("GET", f"/products/{arguments['product_id']}")
            elif name == "list_orders":
                data = await ls.request("GET", "/orders")
            elif name == "get_order":
                data = await ls.request("GET", f"/orders/{arguments['order_id']}")
            elif name == "list_customers":
                data = await ls.request("GET", "/customers")
            elif name == "get_customer":
                data = await ls.request("GET", f"/customers/{arguments['customer_id']}")
            elif name == "list_subscriptions":
                data = await ls.request("GET", "/subscriptions")
            elif name == "get_subscription":
                data = await ls.request("GET", f"/subscriptions/{arguments['subscription_id']}")
            elif name == "list_license_keys":
                data = await ls.request("GET", "/license-keys")
            elif name == "get_license_key":
                data = await ls.request("GET", f"/license-keys/{arguments['license_key_id']}")
            elif name == "create_checkout":
                data = await ls.request("POST", "/checkouts", json_data={"data": arguments["checkout_data"]})
            elif name == "create_webhook":
                data = await ls.request("POST", "/webhooks", json_data={"data": arguments["webhook_data"]})
            else:
                raise ValueError(f"Unknown tool: {name}")

            return [TextContent(type="text", text=json.dumps(data, indent=2))]
        except Exception as e:
            logger.error(f"Tool call failed: {str(e)}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("LemonSqueezy MCP server running...")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="lemonsqueezy-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
        ),
    )
)
        

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
