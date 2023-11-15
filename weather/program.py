from time import sleep

import network
from machine import Pin, Timer

from weather.listener import WeatherStationListener
from weather.mqtt_client import MqttClient
from weather.weather_station import WeatherStation

TIMEOUT = 5000
rocker_pin = Pin(28, Pin.IN, Pin.PULL_UP)


class FakeWatchDog:
    def feed(self):
        print("feeding")


wdt = FakeWatchDog()  # WDT(timeout=TIMEOUT + 3000)  # set a timeout of 3s more
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
    wlan.connect("victoor", "victoor123")
    tries = 0
    while not wlan.isconnected() and wlan.status() >= 0 and tries < 10:
        print("Waiting to connect:")
        flash_led()
        tries = tries + 1
        sleep(2)
        wdt.feed()


def flash_led():
    for i in range(3):
        machine_led.value(1)
        sleep(0.1)
        machine_led.value(0)
        sleep(0.1)


def setup():
    start_up_sequence()
    client = MqttClient()
    station = WeatherStation(listener=WeatherStationListener(client, wdt))
    timer = Timer(-1)
    timer.init(period=TIMEOUT, mode=Timer.PERIODIC, callback=station.notify)

    wdt.feed()  # make sure the watchdog does not shut it down
