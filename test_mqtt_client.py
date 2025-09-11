
import json
import os
import time
import pytest
import logging
from mqtt_client import MCPMQTTClient
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

import sys

@pytest.fixture(scope="module")
def mqtt_client(request):
    config_file = getattr(request, 'param', None)
    broker = os.environ.get("MQTT_BROKER", "localhost")
    port = int(os.environ.get("MQTT_PORT", 1883))
    client_id = os.environ.get("MQTT_CLIENT_ID", "TestClient1")
    username = os.environ.get("MQTT_USERNAME", None)
    password = os.environ.get("MQTT_PASSWORD", None)
    logging.info(f"Using MQTT broker: {broker}, port: {port}, client_id: {client_id}, username: {username}, password: {password}")
    client = MCPMQTTClient(
        broker=broker,
        port=port,
        client_id=client_id,
        username=username,
        password=password
    )
    client.connect()
    yield client
    client.disconnect()

@pytest.mark.parametrize("mqtt_client", [None], indirect=True)
def test_publish_and_receive(mqtt_client):
    import logging
    logging.info("MQTT broker address: %s", mqtt_client.broker)
    logging.info("MQTT broker port: %d", mqtt_client.port)
    logging.info("MQTT client ID: %s", mqtt_client.client_id)
    logging.info("MQTT username: %s", mqtt_client.username)
    logging.info("MQTT password: %s", mqtt_client.password)

    test_topic = "test/mcp/jeee"
    mqtt_client.subscribe(test_topic)
    # Publish several messages
    for i in range(1, 6):
        mqtt_client.publish(test_topic, f"{i}.Hello from MCPMQTTClient!")
    time.sleep(5)  # Wait for messages to be received
    messages = mqtt_client.get_all_received_messages(test_topic)[test_topic]
    assert len(messages) == 5
    # Check that the last message matches
    last_msg = messages[-1][1]
    assert last_msg == "5.Hello from MCPMQTTClient!"
    mqtt_client.publish(test_topic, "Final message")
    time.sleep(2)
    messages = mqtt_client.get_all_received_messages(test_topic)[test_topic]
    assert messages[-1][1] == "Final message"
    assert len(messages) == 5
