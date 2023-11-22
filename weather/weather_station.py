import uasyncio
from machine import I2C, ADC, Pin

from weather.bme680 import BME680_I2C


class WeatherStation:
    def __init__(self, config, listeners=None):
        if listeners is None:
            listeners = []

        self._rocker_count = 0
        self._cumulative_rainfall = 0
        self._rocker_modifier = 0.3274793067734472
        self._scl = config['pins']['bme']['scl']
        self._sda = config['pins']['bme']['sda']
        self._listeners = listeners
        self._rocker_pin = config['pins']['rocker']
        self._rocker_pin.irq(self.tipped, trigger=Pin.IRQ_FALLING)

        self._bme = self.connect_with_bme()
        self._adc = ADC(4)

    def tipped(self, pin):
        print(pin)
        self._rocker_count = self._rocker_count + 1
        print("rocker triggered")

    def connect_with_bme(self):
        i2c = I2C(id=0, scl=self._scl, sda=self._sda)
        return BME680_I2C(i2c=i2c)

    def read_weather_data(self):
        rainfall = self._rocker_count * self._rocker_modifier
        self._cumulative_rainfall = self._cumulative_rainfall + rainfall

        sensor_data = {
            "temperature": self._bme.temperature,
            "humidity": self._bme.humidity,
            "pressure": self._bme.pressure,
            "gas": self._bme.gas,
            "altitude": self._bme.altitude,
            "filter_size": self._bme.filter_size,
            "rainfall": rainfall,
            "cumulative_rainfall": self._cumulative_rainfall,
            "device": {
                "device_temperature": self.calculate_internal_temperature()
            }
        }

        self._rocker_count = self._rocker_count - self._rocker_count

        for listener in self._listeners:
            listener.on_data_received(sensor_data)

    def calculate_internal_temperature(self):
        adc_voltage = self._adc.read_u16() * (3.3 / (65535))
        return 27 - (adc_voltage - 0.706) / 0.001721

    async def start(self, timeout=5000):
        print("starting weather station")
        while True:
            print("reading weather data")
            self.read_weather_data()
            await uasyncio.sleep_ms(timeout)
