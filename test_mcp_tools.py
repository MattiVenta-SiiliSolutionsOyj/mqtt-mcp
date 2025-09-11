import unittest
import time
from mqtt_client import MCPMQTTClient
import json

import os


topic = "test/mcp/jeee"



class TestMCPMQTTClientTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.broker = os.environ.get("MQTT_BROKER", "localhost")
        cls.port = int(os.environ.get("MQTT_PORT", "1883"))
        cls.client_id = os.environ.get("MQTT_CLIENT_ID", "TestClient1")
        cls.username = os.environ.get("MQTT_USERNAME")
        cls.password = os.environ.get("MQTT_PASSWORD")
        cls.client = MCPMQTTClient(
            broker=cls.broker,
            port=cls.port,
            client_id=cls.client_id,
            username=cls.username,
            password=cls.password
        )
        cls.client.connect()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.client.disconnect()

    def test_subscribe_and_get_topics(self):
      
        self.client.subscribe(topic)
        time.sleep(1)
        topics = self.client.get_subscribed_topics()
        self.assertIn(topic, topics)

    def test_get_last_message_none(self):
  
        msg = self.client.get_last_message(topic)
        self.assertTrue(msg is None or isinstance(msg, tuple))

    def test_get_all_received_messages(self):
      
        messages = self.client.get_all_received_messages(topic)
        self.assertIsInstance(messages, dict)
        self.assertIn(topic, messages)

if __name__ == "__main__":
    unittest.main()
