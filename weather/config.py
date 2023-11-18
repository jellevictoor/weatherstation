from machine import Pin

config = {
    'pins': {
        'rocker': Pin(28, Pin.IN, Pin.PULL_UP),
        'bme': {
            'scl': Pin(17),
            'sda': Pin(16)
        },
    },
    'output_file': 'last_weather_reading.json',
    'mqtt': {
        'host': "192.168.1.5",
        'client_id': "weatherstation",
        'topic_pub': b'klskmp/buiten/weather_station/data',
        'status_pub': b'klskmp/buiten/weather_station/status'
    },
    'wifi_ssid': "secret",
    'wifi_password': "secret"
}
