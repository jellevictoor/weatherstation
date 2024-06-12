from machine import Pin

config = {
    'pins': {
        'rocker': Pin(15, Pin.IN, Pin.PULL_UP),
        'bme680': {
            'scl': Pin(5),
            'sda': Pin(4),
        },
        'dht22':{
            'data': Pin(10, Pin.IN),
        }
    },
    'output_file': 'last_weather_reading.json',
    'mqtt': {
        'host': "192.168.1.5",
        'client_id': "weatherstation",
        'topic_pub': b'klskmp/buiten/weather_station/data',
        'status_pub': b'klskmp/buiten/weather_station/status'
    },
    'wifi_ssid': "victoor_iot",
    'wifi_password': "!"
}
