import json
import time

import machine
from umqtt.simple import MQTTClient


class MqttClient:

    def __init__(self, config):
        self._topic_pub = config['mqtt']['topic_pub']
        self._status_pub = config['mqtt']['status_pub']
        self._client = self.init_client(config)
        self._client.publish(self._status_pub, json.dumps({"status": "online"}), retain=True)

    def init_client(self, config):
        host = config['mqtt']['host']
        client_id = config['mqtt']['client_id']
        print("connecting to mqtt broker: %s" % host)
        client = MQTTClient(client_id, host, keepalive=5)
        client.set_last_will(topic=self._status_pub, msg=json.dumps({"status": "offline"}), retain=True, qos=1)
        time.sleep(1)
        client.connect()

        print('Connected to %s MQTT Broker' % host)
        return client

    def publish(self, data):
        try:
            self._client.publish(self._topic_pub, json.dumps(data))
        except OSError as e:
            raise e

