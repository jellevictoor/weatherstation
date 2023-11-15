import json


class WeatherStationListener:
    def __init__(self, mqtt_client, wdt):
        self._mqtt_client = mqtt_client
        self._wdt = wdt

    def on_data_received(self, sensor_data):
        try:
            self._mqtt_client.publish(sensor_data)
            print(json.dumps(sensor_data))
            self._wdt.feed()  # make sure the watchdog does not shut it down
        except OSError as e:
            print("failed to connect")
