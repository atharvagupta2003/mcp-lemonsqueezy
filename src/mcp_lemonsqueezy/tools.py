from mcp.types import Tool

def get_lemonsqueezy_tools() -> list[Tool]:
    return [
        Tool(
            name="get_user",
            description="Get the current authenticated Lemon Squeezy user",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="list_stores",
            description="List all Lemon Squeezy stores",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_store",
            description="Get details of a specific store",
            inputSchema={
                "type": "object",
                "properties": {
                    "store_id": {"type": "string", "description": "The ID of the store"}
                },
                "required": ["store_id"]
            }
        ),
        Tool(
            name="list_products",
            description="List all products",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_product",
            description="Get a specific product by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "The ID of the product"}
                },
                "required": ["product_id"]
            }
        ),
        Tool(
            name="list_orders",
            description="List all orders",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_order",
            description="Get an order by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The ID of the order"}
                },
                "required": ["order_id"]
            }
        ),
        Tool(
            name="list_customers",
            description="List all customers",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_customer",
            description="Get a customer by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "The ID of the customer"}
                },
                "required": ["customer_id"]
            }
        ),
        Tool(
            name="list_subscriptions",
            description="List all subscriptions",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_subscription",
            description="Get a subscription by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "subscription_id": {"type": "string", "description": "The ID of the subscription"}
                },
                "required": ["subscription_id"]
            }
        ),
        Tool(
            name="list_license_keys",
            description="List all license keys",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_license_key",
            description="Get a license key by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "license_key_id": {"type": "string", "description": "The ID of the license key"}
                },
                "required": ["license_key_id"]
            }
        ),
        Tool(
            name="create_checkout",
            description="Create a Lemon Squeezy checkout session",
            inputSchema={
                "type": "object",
                "properties": {
                    "checkout_data": {
                        "type": "object",
                        "description": "Checkout payload as per Lemon Squeezy API"
                    }
                },
                "required": ["checkout_data"]
            }
        ),
        Tool(
            name="create_webhook",
            description="Register a webhook URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "webhook_data": {
                        "type": "object",
                        "description": "Webhook registration payload"
                    }
                },
                "required": ["webhook_data"]
            }
        )
    ]
