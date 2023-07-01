import json
from time import sleep

import network
from machine import Pin, I2C, Timer
from machine import WDT
from umqtt.robust import MQTTClient

from src.weather.bme680 import BME680_I2C

TIMEOUT = 5000
rocker_count = 0
rocker_modifier = 0.3274793067734472
mqtt_server = '192.168.1.5'
client_id = 'weatherstation'
topic_pub = b'klskmp/buiten/weather'
status_pub = b'klskmp/buiten/station'
rocker = Pin(28, Pin.IN, Pin.PULL_UP)
bme = None
client = None

wdt = WDT(timeout=TIMEOUT + 2000)  # set a timeout of 2s more

## calculate surface to benchmark to know the rained mm

# 36 rocks = 300 ml
# rock = 300/36
# surface_in_mm =  pow(180/2,2) * math.pi
# ml_in_mm2 = surface_in_mm/1000
# liter_modifier = rock/ml_in_mm2

machine_led = Pin('LED', Pin.OUT)


def tipped(pin):
    global rocker_count
    rocker_count = rocker_count + 1
    print("rocker triggered")


def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker' % (mqtt_server))
    return client


def send(timer):
    global rocker_count
    machine_led.value(1)
    no_of_rocks_to_send = rocker_count
    temp = round(bme.temperature, 2)
    hum = round(bme.humidity, 2)
    pres = round(bme.pressure, 2)
    gas = round(bme.gas / 1000, 2)
    data_to_send = {
        "rainfall": (no_of_rocks_to_send / 2) * rocker_modifier,  # always triggered twice
        "temp": temp,
        "pressure": pres,
        "humidity": hum,
        "gas": gas
    }
    try:
        client.publish(topic_pub, json.dumps(data_to_send))
        print(json.dumps(data_to_send))
        wdt.feed()  # make sure the watchdog does not shut it down
        machine_led.value(0)
    except OSError as e:
        print("failed to connect")

    rocker_count = rocker_count - no_of_rocks_to_send


def start_up_sequence():
    for i in range(3):
        machine_led.value(1)
        sleep(0.1)
        machine_led.value(0)
        sleep(0.1)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("victoor", "victoor123")
    tries = 0

    while not wlan.isconnected() and wlan.status() >= 0 and tries < 10:
        print("Waiting to connect:")
        for i in range(3):
            machine_led.value(1)
            sleep(0.01)
            machine_led.value(0)
            sleep(0.01)
        tries = tries + 1
        wdt.feed()

    machine_led.value(0)
    print("connected to wlan")
    sleep(3)
    wdt.feed()


def setup():
    global bme
    global client

    start_up_sequence()
    i2c = I2C(id=0, scl=Pin(17), sda=Pin(16))
    bme = BME680_I2C(i2c=i2c)
    client = mqtt_connect()
    client.publish(status_pub, json.dumps({"status": "startup"}))
    wdt.feed()  # make sure the watchdog does not shut it down
    rocker.irq(tipped)
    timer = Timer(-1)
    timer.init(period=TIMEOUT, mode=Timer.PERIODIC, callback=send)

