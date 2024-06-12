from time import sleep

import network
import uasyncio
from machine import Pin, WDT

from weather.config import config
from weather.listeners import WeatherStationListener, FilesystemListener
from weather.mqtt_client import MqttClient
from weather.weather_station import WeatherStation
from weather.webserver import WebServer

TIMEOUT = 5000


class FakeWatchDog:
    def feed(self):
        print("feeding")


# uncomment the WDT line to enable the watchdog
# enabling the watchdog will cause the device to reboot if it is not fed within the timeout
# this can be problematic if you are debugging the device or even pushing new code to it

#wdt = FakeWatchDog()
wdt = WDT(timeout=TIMEOUT + 3000)  # set a timeout of 3s more
machine_led = Pin('LED', Pin.OUT)


def start_up_sequence():
    flash_led()
    connect_wlan()
    machine_led.value(0)
    print("connected to wlan")
    sleep(3)
    wdt.feed()


def connect_wlan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.connect(config['wifi_ssid'], config['wifi_password'])
    tries = 0
    while not wlan.isconnected() and wlan.status() >= 0 and tries < 10:
        print("Waiting to connect:")
        flash_led()
        tries = tries + 1
        sleep(2)
        wdt.feed()
    if not wlan.isconnected():
        raise Exception("Could not connect to wifi")


def flash_led():
    for i in range(3):
        machine_led.value(1)
        sleep(0.1)
        machine_led.value(0)
        sleep(0.1)


async def main_loop():
    loop = uasyncio.get_event_loop()
    client = MqttClient(config)
    server = WebServer(config).listen()
    weather_station = WeatherStation(config, [WeatherStationListener(client, wdt), FilesystemListener(config, wdt)])

    uasyncio.create_task(weather_station.start(TIMEOUT))
    loop.create_task(server)

    wdt.feed()  # make sure the watchdog does not shut it down
    loop.run_forever()


def setup():
    start_up_sequence()
    uasyncio.run(main_loop())
