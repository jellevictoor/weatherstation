import json

from umqtt.simple import MQTTClient


class MqttClient:
    _mqtt_server = '192.168.1.5'
    _client_id = 'weatherstation'
    _topic_pub = b'klskmp/buiten/weather_station/data'
    _status_pub = b'klskmp/buiten/weather_station/status'
    _lst_pub = b'klskmp/buiten/weather_station/lst'

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
