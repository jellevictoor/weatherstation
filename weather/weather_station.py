import uasyncio
from machine import ADC, Pin

from weather.climate_monitor import ClimateMonitor
from weather.sensors import BME680_Sensor, DH22_Sensor


class WeatherStation:
    def __init__(self, config, listeners=None):
        if listeners is None:
            listeners = []

        self._rocker_count = 0
        self._cumulative_rainfall = 0

        self._rocker_modifier = 0.184839525
        bme680_config_data = config['pins']['bme680']
        self._scl = bme680_config_data['scl']
        self._sda = bme680_config_data['sda']

        self._bme680_sensor = BME680_Sensor(scl=bme680_config_data['scl'], sda=bme680_config_data['sda'])
        self._dht22_sensor = DH22_Sensor(data=config['pins']['dht22']['data'])

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

        with ClimateMonitor(self._bme680_sensor, self._dht22_sensor) as climate_monitor:

            dht_22_data = climate_monitor.dht22_sensor.get_data()
            bme680_data = climate_monitor.bme680_sensor.get_data()
            sensor_data = {}
            if dht_22_data is not None:
                sensor_data['dht22'] = dht_22_data
            if bme680_data is not None:
                sensor_data['bme680'] = bme680_data

            sensor_data['device'] = {
                "device_temperature": self.calculate_internal_temperature()
            }

            sensor_data['rainfall'] = {
                "rainfall": rainfall,
                "calibration_value": self._rocker_modifier,
                "cumulative_rainfall": self._cumulative_rainfall,

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
            try:
                self.read_weather_data()
            except Exception as e:
                print("error reading weather data ", e)
            await uasyncio.sleep_ms(timeout)
