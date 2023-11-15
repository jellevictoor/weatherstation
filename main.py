from weather.program import setup
from machine import Pin
from time import sleep

if __name__ == "__main__":
    print("starting up")
    machine_led = Pin('LED', Pin.OUT)
    machine_led.value(1)
    sleep(1)
    machine_led.value(0)
    setup()
