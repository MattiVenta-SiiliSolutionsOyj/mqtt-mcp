#!/bin/bash
# Start a local Eclipse Mosquitto MQTT broker in Docker

docker run -d --name local-mqtt-broker -p 1883:1883 -v "$PWD/mosquitto.conf:/mosquitto/config/mosquitto.conf" eclipse-mosquitto:2.0

# Wait for the broker to be ready
sleep 1

# Run the Python MQTT client test script with local broker parameters and log prints enabled

MQTT_BROKER=localhost MQTT_PORT=1883 .venv/bin/python -m pytest test_mqtt_client.py -v
MQTT_BROKER=localhost MQTT_PORT=1883 .venv/bin/python -m pytest test_mcp_tools.py -v

# Stop and remove the broker container after the test
docker stop local-mqtt-broker
docker rm local-mqtt-broker
