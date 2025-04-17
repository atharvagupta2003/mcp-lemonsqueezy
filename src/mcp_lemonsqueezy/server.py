import os
import json
import logging
import aiohttp
from dotenv import load_dotenv
import mcp.server.stdio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, Resource
from tools import get_lemonsqueezy_tools
from utils import get_auth_headers
from datetime import datetime
from pydantic import AnyUrl

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lemonsqueezy-mcp-server")

class LemonSqueezyManager:
    def __init__(self):
        self.base_url = "https://api.lemonsqueezy.com/v1"
        self.session = aiohttp.ClientSession()
        self.audit_entries = []
    
    def log_operation(self, operation: str, params: dict):
        self.audit_entries.append({
        "timestamp": datetime.utcnow().isoformat(),
        "operation": operation,
        "parameters": params
        })

    def synthesize_audit_log(self) -> str:
        if not self.audit_entries:
           return "No Lemon Squeezy operations logged."
    
        return "\n\n".join([
           f"[{entry['timestamp']}]\nOperation: {entry['operation']}\nParams: {json.dumps(entry['parameters'], indent=2)}"
           for entry in self.audit_entries
        ])


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

    @server.list_resources()
    async def list_resources() -> list[Resource]:
        return [
           Resource(
               uri=AnyUrl("audit://lemonsqueezy-operations"),
               name="Lemon Squeezy Operations Audit Log",
               description="Log of all Lemon Squeezy operations performed through the MCP server",
              mimeType="text/plain",
            )
        ]

    @server.read_resource()
    async def read_resource(uri: AnyUrl) -> str:
        if uri.scheme == "audit" and uri.host == "lemonsqueezy-operations":
            return ls.synthesize_audit_log()
        else:
            raise ValueError(f"Unknown resource URI: {uri}")


    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return get_lemonsqueezy_tools()

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            logger.info(f"Tool: {name}")
            if name == "get_user":
                data = await ls.request("GET", "/users/me")
                ls.log_operation(name, arguments)
            elif name == "list_stores":
                data = await ls.request("GET", "/stores")
                ls.log_operation(name, arguments)
            elif name == "get_store":
                data = await ls.request("GET", f"/stores/{arguments['store_id']}")
                ls.log_operation(name, arguments)
            elif name == "list_products":
                data = await ls.request("GET", "/products")
                ls.log_operation(name, arguments)
            elif name == "get_product":
                data = await ls.request("GET", f"/products/{arguments['product_id']}")
                ls.log_operation(name, arguments)
            elif name == "list_orders":
                data = await ls.request("GET", "/orders")
                ls.log_operation(name, arguments)
            elif name == "get_order":
                data = await ls.request("GET", f"/orders/{arguments['order_id']}")
                ls.log_operation(name, arguments)
            elif name == "list_customers":
                data = await ls.request("GET", "/customers")
                ls.log_operation(name, arguments)
            elif name == "get_customer":
                data = await ls.request("GET", f"/customers/{arguments['customer_id']}")
                ls.log_operation(name, arguments)
            elif name == "list_subscriptions":
                data = await ls.request("GET", "/subscriptions")
                ls.log_operation(name, arguments)
            elif name == "get_subscription":
                data = await ls.request("GET", f"/subscriptions/{arguments['subscription_id']}")
                ls.log_operation(name, arguments)
            elif name == "list_license_keys":
                data = await ls.request("GET", "/license-keys")
                ls.log_operation(name, arguments)
            elif name == "get_license_key":
                data = await ls.request("GET", f"/license-keys/{arguments['license_key_id']}")
                ls.log_operation(name, arguments)
            elif name == "create_checkout":
                data = await ls.request("POST", "/checkouts", json_data={"data": arguments["checkout_data"]})
                ls.log_operation(name, arguments)
            elif name == "create_webhook":
                data = await ls.request("POST", "/webhooks", json_data={"data": arguments["webhook_data"]})
                ls.log_operation(name, arguments)
            elif name == "get_product_variants":
                product_id = arguments["product_id"]
                data = await ls.request("GET", f"/products/{product_id}/variants")
                ls.log_operation(name, arguments)
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
    await ls.close()    
        

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
