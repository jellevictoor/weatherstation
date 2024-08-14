import dht
from machine import Pin
from machine import SoftI2C

from weather.bme680 import BME680_I2C


class BME680_Sensor:
    scl: Pin
    sda: Pin

    def __init__(self, bus: int, scl: Pin, sda: Pin):

        self.__connection = None
        self.bus = bus
        self.scl = scl
        self.sda = sda

    @property
    def is_connected(self):
        return self.__connection is not None

    def connect(self):
        if not self.is_connected:
            print("connecting to", self.__class__)
            try:
                i2c = SoftI2C(scl=self.scl, sda=self.sda)

                found_devices = i2c.scan()
                if found_devices:
                    found_address = found_devices[0]
                    print("found bme680 on address", found_address)
                    self.__connection = BME680_I2C(i2c=i2c, address=found_address)
                    print("connected to bme680")
            except Exception as e:
                print("error connecting to bme680", e)

    def get_data(self):
        if not self.is_connected:
            return
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

    @property
    def is_connected(self):
        return self.__connection is not None

    def connect(self):
        if not self.is_connected:
            print("connecting to", self.__class__)
            try:
                self.__connection = dht.DHT22(self.data)
                print("connected to dht22")
            except Exception as e:
                print("error connecting to dht22", e)

    def get_data(self):
        if not self.is_connected:
            return

        try:
            self.__connection.measure()
            return {
                "temperature": self.__connection.temperature(),
                "humidity": self.__connection.humidity()
            }
        except OSError:
            print("error reading dht22")
            return None
