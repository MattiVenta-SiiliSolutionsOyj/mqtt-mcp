import paho.mqtt.client as mqtt
import time
from collections import defaultdict, deque

class MCPMQTTClient:
    def __init__(self, broker, port=1883, client_id=None, username=None, password=None):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = mqtt.Client(client_id=self.client_id)
        if username and password:
            self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.topics = set()
        self.last_messages = defaultdict(lambda: deque(maxlen=5))  # topic -> deque of (timestamp, message)

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker {self.broker}:{self.port} with result code {rc}")
        # Discover topics by subscribing to wildcard
      



    def subscribe(self, topic):
        self.client.subscribe(topic)
        self.topics.add(topic)
        print(f"Subscribed to topic: {topic}")

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        timestamp = time.time()
        print(f"Received message on topic {msg.topic}: {message}")
        self.last_messages[msg.topic].append((timestamp, message))
    def get_last_message(self, topic=None):
        """Return the last received message for a topic, or None if not available. If topic is None, return messages for all topics."""
        if topic and self.last_messages[topic]:
            return self.last_messages[topic][-1]
        return None

    def get_all_received_messages(self, topic=None):
        """Return all received messages for a specific topic or all topics."""
        if topic:
            return {topic: list(self.last_messages[topic])}
        return {topic: list(messages) for topic, messages in self.last_messages.items()}

    def get_subscribed_topics(self):
        return list(self.topics)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
