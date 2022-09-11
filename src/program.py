import network
import machine
import utime
from machine import Pin, I2C, Timer
from time import sleep
from bme680 import *
from umqtt.robust import MQTTClient
import json

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
    machine_led.value(1)
    global rocker_count
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
        machine_led.value(0)
    except OSError as e:
        print("failed to connect")
        reconnect()

    rocker_count = rocker_count - no_of_rocks_to_send


def start_up_sequence():
    machine_led.value(1)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("victoor", "victoor123")

    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to connect:")
        time.sleep(1)
    machine_led.value(0)


def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()
    # 36 rocks = 0.3 l
    # 1 rock = 0.0083 l
    # rock = 0.3/36
    # surface_in_mm =  pow(180/2,2) * math.pi
    # surface_exploder = 1000000/surface_in_mm
    # liter_modifier = surface_exploder * rock




rocker_count = 0
rocker_modifier = 0.3274793067734472
mqtt_server = '192.168.1.5'
client_id = 'weatherstation'
topic_pub = b'klskmp/buiten/weather'
rocker = Pin(18, Pin.IN, Pin.PULL_UP)
bme = None
client = None


def setup():
    global bme
    global client

    start_up_sequence()
    i2c = I2C(id=0, scl=Pin(17), sda=Pin(16))
    bme = BME680_I2C(i2c=i2c)
    client = mqtt_connect()
    rocker.irq(tipped)
    timer = Timer(-1)
    timer.init(period=5000, mode=Timer.PERIODIC, callback=send)
