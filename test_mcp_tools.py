import unittest
import time
from mqtt_client import MCPMQTTClient
import json

import os
CONFIG_FILE = "mqtt-conf.json"
DEFAULT_CONFIG_FILE = "mqtt-conf-default.json"

def get_config_file():
    return CONFIG_FILE if os.path.exists(CONFIG_FILE) else DEFAULT_CONFIG_FILE

class TestMCPMQTTClientTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(get_config_file(), "r") as f:
            cls.config = json.load(f)
        cls.client = MCPMQTTClient(
            broker=cls.config["MQTT_BROKER"],
            port=cls.config.get("MQTT_PORT", 1883),
            client_id=cls.config.get("MQTT_CLIENT_ID"),
            username=cls.config.get("MQTT_USERNAME"),
            password=cls.config.get("MQTT_PASSWORD")
        )
        cls.client.connect()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.client.disconnect()

    def test_subscribe_and_get_topics(self):
        topic = self.config.get("MQTT_TEST_TOPIC", "test/#")
        self.client.subscribe(topic)
        time.sleep(1)
        topics = self.client.get_subscribed_topics()
        self.assertIn(topic, topics)

    def test_get_last_message_none(self):
        topic = self.config.get("MQTT_TEST_TOPIC", "test/#")
        msg = self.client.get_last_message(topic)
        self.assertTrue(msg is None or isinstance(msg, tuple))

    def test_get_all_received_messages(self):
        topic = self.config.get("MQTT_TEST_TOPIC", "test/#")
        messages = self.client.get_all_received_messages(topic)
        self.assertIsInstance(messages, dict)
        self.assertIn(topic, messages)

if __name__ == "__main__":
    unittest.main()
