# Lemon Squeezy Server
[![smithery badge](https://smithery.ai/badge/@atharvagupta2003/mcp-lemonsqueezy)](https://smithery.ai/server/@atharvagupta2003/mcp-lemonsqueezy)

A Model Context Protocol (MCP) server implementation that integrates with [Lemon Squeezy](https://www.lemonsqueezy.com/) for handling subscriptions, checkouts, products, and more. This server provides a structured interface to programmatically manage your Lemon Squeezy store with audit logging and tool-based control.


# Demo
![lemonsqueezy_demo](https://github.com/user-attachments/assets/ad2372c2-adfd-4a3f-b300-005d5f175b85)


## Requirements
- Python 3.8+
- MCP SDK 0.1.0+
- aiohttp
- python-dotenv

## Components

### Resources
The server provides an MCP-compatible resource for operation auditing:

- Stores logs of all tool-based Lemon Squeezy operations
- Exposes audit log via `read_resource` endpoint
- Helpful for debugging and audit traceability

### Tools
Implements a full set of Lemon Squeezy operations via MCP tools:

#### 🔍 Store & Product Tools
- `get_user`: Get current Lemon Squeezy user info  
- `list_stores`: List all stores  
- `get_store`: Fetch a specific store  
- `list_products`: List products  
- `get_product`: Get product details  
- `get_product_variants`: List variants for a product  

#### 📦 Order & Customer Tools
- `list_orders`: List all orders  
- `get_order`: Get details of an order  
- `list_customers`: List all customers  
- `get_customer`: Fetch customer details  

#### 💳 Subscription & License Tools
- `list_subscriptions`: List subscriptions  
- `get_subscription`: Get a subscription  
- `list_license_keys`: List license keys  
- `get_license_key`: Fetch license key info  

#### 🛒 Checkout & Webhook Tools
- `create_checkout`: Create a fully customized checkout session  
- `create_webhook`: Register a new webhook  
- `list_webhooks`: List all webhooks (filterable by store)

---

## Features
- **Subscription & Checkout Management**
- **Webhook Creation & Listing**
- **Audit Logging of All Actions**
- **MCP-Compatible Tool & Resource Integration**
- **Error Feedback and Logging**

---

## Installation

### Installing via Smithery

To install LemonSqueezy Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@atharvagupta2003/mcp-lemonsqueezy):

```bash
npx -y @smithery/cli install @atharvagupta2003/mcp-lemonsqueezy --client claude
```

### Install dependencies
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
pip install -e .
```

### Configuration
Set up the environment variables in a `.env` file:
```sh
LEMON_SQUEEZY_API_KEY=your_lemonsqueezy_api_key
```

#### Claude Desktop

Add the server configuration to your Claude Desktop config:

Windows: C:\Users\<username>\AppData\Roaming\Claude\claude_desktop_config.json

MacOS: ~/Library/Application Support/Claude/claude_desktop_config.json

```
{
  "mcpServers": {
    "lemonsqueezy": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/src/mcp_lemonsqueezy/",
        "run",
        "server.py"
      ]
    }
  }
}
```

## Usage

### Start the server
```sh
uv run src/mcp_lemonsqueezy/server.py
```


### Example MCP Commands

#### Get Current User
```json
{
  "tool": "get_user",
  "arguments": {}
}

```

#### List All Stores
```json
{
  "tool": "list_stores",
  "arguments": {}
}

```

#### Get a Store by ID
```json
{
  "tool": "get_store",
  "arguments": {
    "store_id": "164870"
  }
}

```


## Error Handling
The server provides clear error messages for common scenarios:
- **401 Unauthorized**: Missing or invalid API key
- **422 Unprocessable Entity**: Invalid fields like missing variant/store ID
- **400 Bad Request**: Invalid JSON API structure

## Development
### Testing
Run the MCP Inspector for interactive testing:
```sh
npx @modelcontextprotocol/inspector uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/src/mcp_lemonsqueezy run server.py
```

### Building
1. Update dependencies:
```
uv compile pyproject.toml
```
2. Build package:
```
uv build
```

### Contributing
We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
