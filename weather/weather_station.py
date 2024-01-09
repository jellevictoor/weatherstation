import uasyncio
from machine import ADC, Pin

from weather.climate_monitor import ClimateMonitor


class WeatherStation:
    def __init__(self, config, listeners=None):
        if listeners is None:
            listeners = []

        self._rocker_count = 0
        self._cumulative_rainfall = 0

        self._rocker_modifier = 0.19044181224671242
        self.temperature_correction = 2.3221693163561645
        self._scl = config['pins']['bme']['scl']
        self._sda = config['pins']['bme']['sda']
        self._vin = config['pins']['bme']['vin']
        self._listeners = listeners
        self._rocker_pin = config['pins']['rocker']
        self._rocker_pin.irq(self.tipped, trigger=Pin.IRQ_FALLING)

        self._adc = ADC(4)

    def tipped(self, pin):
        print(pin)
        self._rocker_count = self._rocker_count + 1
        print("rocker triggered")

    def read_weather_data(self):
        rainfall = self._rocker_count * self._rocker_modifier
        self._cumulative_rainfall = self._cumulative_rainfall + rainfall

        with ClimateMonitor(self._vin, self._scl, self._sda) as climate_monitor:
            sensor_data = {
                "raw_temperature": climate_monitor.get_temperature(),
                "temperature": climate_monitor.get_temperature() - self.temperature_correction,
                "humidity": climate_monitor.get_humidity(),
                "pressure": climate_monitor.get_pressure(),
                "gas": climate_monitor.get_gas(),
                "altitude": climate_monitor.get_altitude(),
                "filter_size": climate_monitor.get_filter_size(),
                "rainfall": rainfall,
                "calibration_value": self._rocker_modifier,
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
