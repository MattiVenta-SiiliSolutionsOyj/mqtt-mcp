import json
from mqtt_client import MCPMQTTClient

import os
CONFIG_FILE = "mqtt-conf.json"
DEFAULT_CONFIG_FILE = "mqtt-conf-default.json"

def get_config_file():
    return CONFIG_FILE if os.path.exists(CONFIG_FILE) else DEFAULT_CONFIG_FILE

def load_config():
    with open(get_config_file(), "r") as f:
        return json.load(f)

def main():
    config = load_config()
    print("Loaded config:", config)
    print("MQTT Broker:", config["MQTT_BROKER"])
    print("MQTT Port:", config["MQTT_PORT"])
    print("MQTT Username:", config["MQTT_USERNAME"])
    print("MQTT Password:", config["MQTT_PASSWORD"])
    print("MQTT Client ID:", config["MQTT_CLIENT_ID"])
    print("MQTT Test Topic:", config["MQTT_TEST_TOPIC"])

    client = MCPMQTTClient(
        broker=config["MQTT_BROKER"],
        port=config.get("MQTT_PORT", 1883),
        client_id=config.get("MQTT_CLIENT_ID"),
        username=config.get("MQTT_USERNAME"),
        password=config.get("MQTT_PASSWORD")
    )
    client.connect()
    client.subscribe(config.get("MQTT_TEST_TOPIC", "test/#"))
    import time
    time.sleep(5)  # Wait for messages
    print("Subscribed topics:", client.get_subscribed_topics())
    for topic in client.get_subscribed_topics():
        print(f"Last message for {topic}: {client.get_last_message(topic)}")
    client.disconnect()

if __name__ == "__main__":
    main()
