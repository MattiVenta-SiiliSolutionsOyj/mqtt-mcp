from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mqtt-mcp")

@mcp.tool()
def get_mqtt_data(data: Any) -> str:
    """Process and return MQTT data."""
    return f"Processed MQTT data: jeee"



if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')