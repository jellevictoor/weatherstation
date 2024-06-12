from weather.sensors import BME680_Sensor, DH22_Sensor


class ClimateMonitor:
    def __init__(self, bme680_sensor: BME680_Sensor, dht22_sensor: DH22_Sensor):
        self.bme680_sensor = bme680_sensor
        self.dht22_sensor = dht22_sensor

    def __enter__(self):
        print("connecting to sensors")
        self.bme680_sensor.connect()
        self.dht22_sensor.connect()
        return self

    def get_temperature(self) -> dict[str, float]:
        return {
            "bme680": self.bme680_sensor.temperature,
            "dht22": self.dht22_sensor.temperature
        }

    def get_humidity(self):
        return {
            "bme680": self.bme680_sensor.humidity,
            "dht22": self.dht22_sensor.humidity
        }

    def get_pressure(self):
        return {
            "bme680": self.bme680_sensor.pressure,
        }

    def get_gas(self):
        return {
            "bme680": self.bme680_sensor.gas,
        }

    def get_altitude(self):
        return {
            "bme680": self.bme680_sensor.altitude,
        }

    def get_filter_size(self):
        return {
            "bme680": self.bme680_sensor.filter_size,
        }

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
