import os
import json
import logging
from datetime import datetime
from typing import Any
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from pydantic import AnyUrl
from utils import get_auth_headers

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lemonsqueezy-fastmcp-server")

LEM_SQ_API_BASE = "https://api.lemonsqueezy.com/v1"

# Audit log manager
class AuditLog:
    def __init__(self):
        self.entries = []

    def log(self, operation: str, params: dict):
        self.entries.append({
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "parameters": params
        })

    def synthesize(self) -> str:
        if not self.entries:
            return "No Lemon Squeezy operations logged."
        return "\n\n".join([
            f"[{entry['timestamp']}]\nOperation: {entry['operation']}\nParams: {json.dumps(entry['parameters'], indent=2)}"
            for entry in self.entries
        ])

audit_log = AuditLog()

# HTTP request helper
async def lemonsqueezy_request(method: str, endpoint: str, params: dict = None, json_data: dict = None) -> Any:
    url = f"{LEM_SQ_API_BASE}{endpoint}"
    headers = get_auth_headers()
    async with httpx.AsyncClient() as client:
        resp = await client.request(method, url, headers=headers, params=params, json=json_data)
        if resp.status_code >= 400:
            raise Exception(f"{resp.status_code}: {resp.text}")
        return resp.json()

# FastMCP server instance
description = "LemonSqueezy MCP server exposing LemonSqueezy API as MCP tools and an audit log as a resource."
mcp = FastMCP(
    "lemonsqueezy-mcp",
    version="0.2.0",
    description=description
)

# Resource: Audit log
@mcp.resource("audit://lemonsqueezy-operations")
async def lemonsqueezy_audit_log() -> str:
    """
    Log of all Lemon Squeezy operations performed through the MCP server.
    """
    return audit_log.synthesize()

# Tool: get_user
@mcp.tool()
async def get_user(ctx: Context) -> dict:
    """
    Get the current authenticated Lemon Squeezy user.
    """
    data = await lemonsqueezy_request("GET", "/users/me")
    audit_log.log("get_user", {})
    return data

@mcp.tool()
async def list_stores(ctx: Context) -> dict:
    """
    List all Lemon Squeezy stores.
    """
    data = await lemonsqueezy_request("GET", "/stores")
    audit_log.log("list_stores", {})
    return data

@mcp.tool()
async def get_store(store_id: str, ctx: Context) -> dict:
    """
    Get details of a specific store.
    Args:
        store_id: The ID of the store
    """
    data = await lemonsqueezy_request("GET", f"/stores/{store_id}")
    audit_log.log("get_store", {"store_id": store_id})
    return data

@mcp.tool()
async def list_products(ctx: Context) -> dict:
    """
    List all products.
    """
    data = await lemonsqueezy_request("GET", "/products")
    audit_log.log("list_products", {})
    return data

@mcp.tool()
async def get_product(product_id: str, ctx: Context) -> dict:
    """
    Get a specific product by ID.
    Args:
        product_id: The ID of the product
    """
    data = await lemonsqueezy_request("GET", f"/products/{product_id}")
    audit_log.log("get_product", {"product_id": product_id})
    return data

@mcp.tool()
async def get_product_variants(product_id: str, ctx: Context) -> dict:
    """
    Get all variants for a given product ID.
    Args:
        product_id: The ID of the product to fetch variants for
    """
    data = await lemonsqueezy_request("GET", f"/products/{product_id}/variants")
    audit_log.log("get_product_variants", {"product_id": product_id})
    return data

@mcp.tool()
async def list_orders(ctx: Context) -> dict:
    """
    List all orders.
    """
    data = await lemonsqueezy_request("GET", "/orders")
    audit_log.log("list_orders", {})
    return data

@mcp.tool()
async def get_order(order_id: str, ctx: Context) -> dict:
    """
    Get an order by ID.
    Args:
        order_id: The ID of the order
    """
    data = await lemonsqueezy_request("GET", f"/orders/{order_id}")
    audit_log.log("get_order", {"order_id": order_id})
    return data

@mcp.tool()
async def list_customers(ctx: Context) -> dict:
    """
    List all customers.
    """
    data = await lemonsqueezy_request("GET", "/customers")
    audit_log.log("list_customers", {})
    return data

@mcp.tool()
async def get_customer(customer_id: str, ctx: Context) -> dict:
    """
    Get a customer by ID.
    Args:
        customer_id: The ID of the customer
    """
    data = await lemonsqueezy_request("GET", f"/customers/{customer_id}")
    audit_log.log("get_customer", {"customer_id": customer_id})
    return data

@mcp.tool()
async def list_subscriptions(ctx: Context) -> dict:
    """
    List all subscriptions.
    """
    data = await lemonsqueezy_request("GET", "/subscriptions")
    audit_log.log("list_subscriptions", {})
    return data

@mcp.tool()
async def get_subscription(subscription_id: str, ctx: Context) -> dict:
    """
    Get a subscription by ID.
    Args:
        subscription_id: The ID of the subscription
    """
    data = await lemonsqueezy_request("GET", f"/subscriptions/{subscription_id}")
    audit_log.log("get_subscription", {"subscription_id": subscription_id})
    return data

@mcp.tool()
async def list_license_keys(ctx: Context) -> dict:
    """
    List all license keys.
    """
    data = await lemonsqueezy_request("GET", "/license-keys")
    audit_log.log("list_license_keys", {})
    return data

@mcp.tool()
async def get_license_key(license_key_id: str, ctx: Context) -> dict:
    """
    Get a license key by ID.
    Args:
        license_key_id: The ID of the license key
    """
    data = await lemonsqueezy_request("GET", f"/license-keys/{license_key_id}")
    audit_log.log("get_license_key", {"license_key_id": license_key_id})
    return data

@mcp.tool()
async def create_checkout(data: dict, ctx: Context) -> dict:
    """
    Create a Lemon Squeezy checkout session with full custom configuration.
    Args:
        data: The checkout data (see LemonSqueezy API docs)
    """
    result = await lemonsqueezy_request("POST", "/checkouts", json_data={"data": data})
    audit_log.log("create_checkout", {"data": data})
    return result

@mcp.tool()
async def create_webhook(webhook_data: dict, ctx: Context) -> dict:
    """
    Register a webhook URL for a specific store and events.
    Args:
        webhook_data: The webhook data (see LemonSqueezy API docs)
    """
    result = await lemonsqueezy_request("POST", "/webhooks", json_data=webhook_data)
    audit_log.log("create_webhook", {"webhook_data": webhook_data})
    return result

@mcp.tool()
async def list_webhooks(store_id: str = None, ctx: Context = None) -> dict:
    """
    List all webhooks. Optionally filter by store ID.
    Args:
        store_id: If provided, only webhooks for this store will be returned
    """
    params = {"filter[store_id]": store_id} if store_id else None
    data = await lemonsqueezy_request("GET", "/webhooks", params=params)
    audit_log.log("list_webhooks", {"store_id": store_id})
    return data

if __name__ == "__main__":
    mcp.run()