import dht
from machine import I2C
from machine import Pin

from weather.bme680 import BME680_I2C


class BME680_Sensor:
    scl: Pin
    sda: Pin

    def __init__(self, scl: Pin, sda: Pin):
        self.__connection = None
        self.scl = scl
        self.sda = sda

    def connect(self):
        if self.__connection is None:
            i2c = I2C(id=0, scl=self.scl, sda=self.sda)
            self.__connection = BME680_I2C(i2c=i2c)
            print("connected to bme680")

    @property
    def temperature(self):
        return self.__connection.temperature

    @property
    def humidity(self):
        return self.__connection.humidity

    @property
    def pressure(self):
        return self.__connection.pressure

    @property
    def gas(self):
        return self.__connection.gas

    @property
    def filter_size(self):
        return self.__connection.filter_size

    @property
    def altitude(self):
        return self.__connection.altitude

    def get_data(self):
        try:
            return {
                "temperature": self.__connection.temperature,
                "humidity": self.__connection.humidity,
                "pressure": self.__connection.pressure,
                "gas": self.__connection.gas,
                "filter_size": self.__connection.filter_size,
                "altitude": self.__connection.altitude
            }
        except OSError:
            print("error reading bme680")
            return None


class DH22_Sensor:
    data: Pin

    def __init__(self, data: Pin):
        self.data = data
        self.__connection = None

    def connect(self):
        if self.__connection is None:
            self.__connection = dht.DHT22(self.data)
            print("connected to dht22")

    @property
    def temperature(self):
        self.__connection.measure()
        return self.__connection.temperature()

    @property
    def humidity(self):
        self.__connection.measure()
        return self.__connection.humidity()

    def get_data(self):
        try:
            self.__connection.measure()
            return {
                "temperature": self.__connection.temperature(),
                "humidity": self.__connection.humidity()
            }
        except OSError:
            print("error reading dht22")
            return None
