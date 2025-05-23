# Use the Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and uv.lock files
COPY pyproject.toml uv.lock /app/

# Install the dependencies
RUN pip install --no-cache-dir uv

# Copy the application code
COPY src /app/src

# Set environment variables
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Ensure that .venv/bin is in the PATH to access installed packages
ENV PATH="/app/.venv/bin:$PATH"

# Copy .env.example to .env (to be configured with actual values in practice)
COPY .env.example .env

# Run the MCP server
ENTRYPOINT ["uv", "run", "src/mcp_lemonsqueezy/server.py"]
