import time

from machine import I2C

from weather.bme680 import BME680_I2C


class ClimateMonitor:
    def __init__(self, vin, scl, sda):
        self._vin = vin
        self._sda = sda
        self._scl = scl
        self._bme = None

    def __enter__(self):
        self._vin.on()  # turn on
        time.sleep(1)  # wait a bit :/
        i2c = I2C(id=0, scl=self._scl, sda=self._sda)
        self._bme = BME680_I2C(i2c=i2c)
        return self

    def get_temperature(self):
        return self._bme.temperature

    def get_humidity(self):
        return self._bme.humidity

    def get_pressure(self):
        return self._bme.pressure

    def get_gas(self):
        return self._bme.gas

    def get_altitude(self):
        return self._bme.altitude

    def get_filter_size(self):
        return self._bme.filter_size

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._vin.off()
