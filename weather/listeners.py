import json
import machine

class FilesystemListener():
    def __init__(self, config, wdt):
        self._wdt = wdt
        self._output_file = config['output_file']

    def on_data_received(self, sensor_data):
        with open(self._output_file, 'w') as outfile:
            json.dump(sensor_data, outfile)
        self._wdt.feed()


class WeatherStationListener():
    def __init__(self, mqtt_client, wdt):
        self._mqtt_client = mqtt_client
        self._wdt = wdt

    def on_data_received(self, sensor_data):
        try:
            self._mqtt_client.publish(sensor_data)
            self._wdt.feed()  # make sure the watchdog does not shut it down
        except OSError as e:
            print("failed to connect")
            machine.soft_reset()
