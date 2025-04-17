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
            name="get_product_variants",
            description="Get all variants for a given product ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The ID of the product to fetch variants for"
                    }
                },
                "required": ["product_id"]
            }
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
            description="Create a Lemon Squeezy checkout session with full custom configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["checkouts"]
                            },
                            "attributes": {
                                "type": "object",
                                "properties": {
                                    "custom_price": {
                                        "type": "integer",
                                        "description": "Price in cents (e.g., 9900 for $99.00)"
                                    },
                                    "product_options": {
                                        "type": "object",
                                        "properties": {
                                            "enabled_variants": {
                                                "type": "array",
                                                "items": {"type": "integer"}
                                            },
                                            "redirect_url": {"type": "string"},
                                            "receipt_thank_you_note": {"type": "string"},
                                            "receipt_button_text": {"type": "string"},
                                            "receipt_link_url": {"type": "string"}
                                        }
                                    },
                                    "checkout_options": {
                                        "type": "object",
                                        "properties": {
                                            "button_color": {"type": "string"}
                                        }
                                    },
                                    "checkout_data": {
                                        "type": "object",
                                        "properties": {
                                            "email": {"type": "string"},
                                            "name": {"type": "string"},
                                            "discount_code": {"type": "string"},
                                            "custom_notes": {"type": "string"},
                                            "custom": {
                                                "type": "object",
                                                "properties": {
                                                    "user_id": {"type": "string"}
                                                }
                                            }
                                        },
                                        "required": ["email", "name"]
                                    },
                                    "expires_at": {
                                        "type": "string",
                                        "format": "date-time"
                                    },
                                    "preview": {
                                        "type": "boolean"
                                    }
                                },
                                "required": ["product_options", "checkout_data"]
                            },
                            "relationships": {
                                "type": "object",
                                "properties": {
                                    "store": {
                                        "type": "object",
                                        "properties": {
                                            "data": {
                                                "type": "object",
                                                "properties": {
                                                    "type": {
                                                        "type": "string",
                                                        "enum": ["stores"]
                                                    },
                                                    "id": {"type": "string"}
                                                },
                                                "required": ["type", "id"]
                                            }
                                        },
                                        "required": ["data"]
                                    },
                                    "variant": {
                                        "type": "object",
                                        "properties": {
                                            "data": {
                                                "type": "object",
                                                "properties": {
                                                    "type": {
                                                        "type": "string",
                                                        "enum": ["variants"]
                                                    },
                                                    "id": {"type": "string"}
                                                },
                                                "required": ["type", "id"]
                                            }
                                        },
                                        "required": ["data"]
                                    }
                                },
                                "required": ["store", "variant"]
                            }
                        },
                        "required": ["type", "attributes", "relationships"]
                    }
                },
                "required": ["data"]
            }
        ),
        Tool(
            name="create_webhook",
            description="Register a webhook URL for a specific store and events",
            inputSchema={
                "type": "object",
                "properties": {
                    "webhook_data": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["webhooks"]
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "url": {"type": "string"},
                                            "events": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            },
                                            "secret": {"type": "string"}
                                        },
                                        "required": ["url", "events", "secret"]
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "properties": {
                                            "store": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "enum": ["stores"]
                                                            },
                                                            "id": {
                                                                "type": "string",
                                                                "description": "The store ID"
                                                            }
                                                        },
                                                        "required": ["type", "id"]
                                                    }
                                                },
                                                "required": ["data"]
                                            }
                                        },
                                        "required": ["store"]
                                    }
                                },
                                "required": ["type", "attributes", "relationships"]
                            }
                        },
                        "required": ["data"]
                    }
                },
                "required": ["webhook_data"]
            }
        ),
        Tool(
            name="list_webhooks",
            description="List all webhooks. Optionally filter by store ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "store_id": {
                        "type": "string",
                        "description": "If provided, only webhooks for this store will be returned"
                    }
                }
            }
        )
]
