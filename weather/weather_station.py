from machine import Pin, I2C

from weather.bme680 import BME680_I2C


class WeatherStation:
    def __init__(self, scl=Pin(17), sda=Pin(16), listener=None):
        self._rocker_count = 0
        self._rocker_modifier = 0.3274793067734472
        self._scl = scl
        self._sda = sda
        self._listener = listener
        self._rocker_pin = Pin(28, Pin.IN, Pin.PULL_UP)
        self._rocker_pin.irq(self.tipped)
        self._bme = self.connect_with_bme()

    def tipped(self, pin):
        self._rocker_count = self._rocker_count + 1
        print("rocker triggered")

    def connect_with_bme(self):
        i2c = I2C(id=0, scl=self._scl, sda=self._sda)
        return BME680_I2C(i2c=i2c)

    def notify(self, timer):
        rainfall = (self._rocker_count / 2) * self._rocker_modifier  # always triggered twice
        sensor_data = {
            "temperature": self._bme.temperature,
            "humidity": self._bme.humidity,
            "pressure": self._bme.pressure,
            "gas": self._bme.gas,
            "altitude": self._bme.altitude,
            "rainfall": rainfall
        }
        self._rocker_count = self._rocker_count - self._rocker_count
        self._listener.on_data_received(sensor_data)
