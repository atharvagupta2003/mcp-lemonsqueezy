from . import server
import asyncio

def main():
    """Entry point for the Lemon Squeezy MCP server."""
    asyncio.run(server.main())

__all__ = ['main', 'server']
