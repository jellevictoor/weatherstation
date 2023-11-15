import json

from umqtt.simple import MQTTClient

from weather.config import config


class MqttClient:
    _mqtt_server = config['mqtt']['host']
    _client_id = config['mqtt']['client_id']
    _topic_pub = config['mqtt']['topic_pub']
    _status_pub = config['mqtt']['status_pub']

    def __init__(self):
        self._client = MQTTClient(self._client_id, self._mqtt_server, keepalive=5)
        self._client.set_last_will(topic=self._status_pub, msg=json.dumps({"status": "offline"}), retain=True, qos=1)
        self._client.connect()
        print('Connected to %s MQTT Broker' % self._mqtt_server)
        self._client.publish(self._status_pub, json.dumps({"status": "online"}), retain=True)

    def publish(self, data):
        try:
            self._client.publish(self._topic_pub, json.dumps(data))
        except OSError as e:
            print("failed to connect")
