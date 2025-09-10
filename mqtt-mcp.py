from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import json
import os

from mqtt_client import MCPMQTTClient
import time

# Load MQTT config from mqtt_config.json or fallback to mqtt_config_default.json
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'mqtt-conf.json')
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'mqtt-conf-default.json')
default_config = {}

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as f:
        default_config = json.load(f)
elif os.path.exists(DEFAULT_CONFIG_PATH):
    with open(DEFAULT_CONFIG_PATH, 'r') as f:
        default_config = json.load(f)

MQTT_BROKER = default_config.get('MQTT_BROKER', 'localhost')
MQTT_PORT = default_config.get('MQTT_PORT', 1883)
MQTT_USERNAME = default_config.get('MQTT_USERNAME')
MQTT_PASSWORD = default_config.get('MQTT_PASSWORD')

# Initialize FastMCP server
mcp = FastMCP("mqtt-mcp")

mqtt_client_instance = None



@mcp.tool()
def connect_mqtt_server(broker: str= MQTT_BROKER, port: int = MQTT_PORT, username: str = MQTT_USERNAME, password: str = MQTT_PASSWORD) -> str:
    """Connect to the MQTT server."""
    global mqtt_client_instance
    mqtt_client_instance = MCPMQTTClient(broker, port, username=username, password=password)
    mqtt_client_instance.connect()
    return f"Connected to MQTT server at {broker}:{port}"

@mcp.tool()
def disconnect_mqtt_server() -> str:
    """Disconnect from the MQTT server."""
    global mqtt_client_instance
    if mqtt_client_instance:
        mqtt_client_instance.disconnect()
        mqtt_client_instance = None
        return "Disconnected from MQTT server."
    return "No MQTT connection to disconnect."



@mcp.tool()
def subscribe_mqtt_topic(topic: str) -> str:
    """Subscribe to a topic on the MQTT server."""
    global mqtt_client_instance
    if mqtt_client_instance:
        mqtt_client_instance.subscribe(topic)
        return f"Subscribed to topic: {topic}"
    return "MQTT client is not connected."


@mcp.tool()
def get_topic_last_value(topic: str) -> str:
    """Get the last received message for a topic."""
    global mqtt_client_instance
    if mqtt_client_instance:
        value = mqtt_client_instance.get_last_message(topic)
        if value is not None:
            return f"Last value for topic '{topic}': {value}"
        else:
            return f"No message received yet for topic '{topic}'."
    return "MQTT client is not connected."


@mcp.tool()
def unsubscribe_mqtt_topic(topic: str) -> str:
    """Unsubscribe from a topic on the MQTT server."""
    global mqtt_client_instance
    if mqtt_client_instance:
        mqtt_client_instance.client.unsubscribe(topic)
        mqtt_client_instance.topics.discard(topic)
        return f"Unsubscribed from topic: {topic}"
    return "MQTT client is not connected."


@mcp.tool()
def get_subscribed_topics() -> str:
    """Get all currently subscribed topics."""
    global mqtt_client_instance
    if mqtt_client_instance:
        topics = mqtt_client_instance.get_subscribed_topics()
        return f"Subscribed topics: {topics}"
    return "MQTT client is not connected."

@mcp.tool()
def subscribe_to_wildcard() -> str:
    """Subscribe to a wildcard topic on the MQTT server."""
    global mqtt_client_instance
    if mqtt_client_instance:
        mqtt_client_instance.subscribe("#")
        return f"Subscribed to wildcard topic: #"
    return "MQTT client is not connected."

@mcp.tool()
def get_received_topics() -> str:
    """Get all topics that have received messages."""
    global mqtt_client_instance
    if mqtt_client_instance:
        topics = list(mqtt_client_instance.last_messages.keys())
        return f"Received topics: {topics}"
    return "MQTT client is not connected."
@mcp.tool()
def get_all_received_messages(topic: str) -> str:
        """Get all received messages (with timestamps) for a specific topic."""
        global mqtt_client_instance
        if mqtt_client_instance:
            messages = mqtt_client_instance.last_messages.get(topic)
            if messages is not None:
                return f"All received messages for topic '{topic}': {list(messages)}"
            else:
                return f"No messages received yet for topic '{topic}'."
        return "MQTT client is not connected."



if __name__ == "__main__":
    # Initialize and run the server
    mcp.run()