import json
import time
import machine
from umqtt.simple import MQTTClient

class MqttClient:

    def __init__(self, config):
        self._topic_pub = config['mqtt']['topic_pub']
        self._status_pub = config['mqtt']['status_pub']
        self._host = config['mqtt']['host']
        self._client_id = config['mqtt']['client_id']
        self._keepalive = config.get('mqtt').get('keepalive', 5)  # Set a default keepalive value
        self._client = self.init_client()

    def init_client(self):
        client = MQTTClient(self._client_id, self._host, keepalive=self._keepalive)
        client.set_last_will(self._status_pub, json.dumps({"status": "offline"}), retain=True, qos=1)
        return client

    def connect(self):
        try:
            self._client.connect()
            print(f'Connected to {self._host} MQTT Broker')
        except OSError as e:
            print("Failed to connect", e)
            raise e

    def disconnect(self):
        self._client.disconnect()
        print('Disconnected from MQTT Broker')

    def publish(self, data):
        try:
            self.connect()
            self._client.publish(self._status_pub, json.dumps({"status": "online"}), retain=True)
            self._client.publish(self._topic_pub, json.dumps(data))
            self._client.publish(self._status_pub, json.dumps({"status": "offline"}), retain=True)
            self.disconnect()
        except OSError as e:
            print("Failed to publish", e)
            raise e

