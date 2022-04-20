#!/usr/bin/python3
import interrupt_client
import ds18b20_therm
import bme280_sensor
import wind_direction_byo
import database 

from prometheus_client import start_http_server, Summary, Gauge
import random
import time

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
TEST_GAUGE = Gauge('weather_metrics', 'Tasty home weather', ['metric'])
TEST_GAUGE.labels('ambient_temp')
TEST_GAUGE.labels('ground_temp')
TEST_GAUGE.labels('humidity')
TEST_GAUGE.labels('pressure')
TEST_GAUGE.labels('wind_speed')
TEST_GAUGE.labels('wind_gust')
TEST_GAUGE.labels('wind_direction')
TEST_GAUGE.labels('rainfall')

TEMP_PROBE = ds18b20_therm.DS18B20()

# Set-up weather objects
WIND_VANE = wind_direction_byo
INTERRUPTS = interrupt_client.interrupt_client(port = 49501)

GLOBAL_SLEEP = 10

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)

# @TEST_GAUGE.time()
def poll_bme():
    humidity, pressure, ambient_temp = bme280_sensor.read_all()
    TEST_GAUGE.labels('humidity').set(humidity)
    TEST_GAUGE.labels('pressure').set(pressure)
    TEST_GAUGE.labels('ambient_temp').set(ambient_temp)
    return 0

def poll_temp():
    TEST_GAUGE.labels('ground_temp').set(TEMP_PROBE.read_temp())
    return 0

def poll_wind():
    wind_avg_direction = round(WIND_VANE.get_value(10), 2) # ten seconds
    wind_speed = INTERRUPTS.get_wind(round_it=True)
    wind_gust = INTERRUPTS.get_wind_gust(round_it=True)
    # Bad wind directions are captured as being 999.99...
    if wind_avg_direction != 999.99:
        TEST_GAUGE.labels('wind_direction').set(wind_avg_direction)
    TEST_GAUGE.labels('wind_speed').set(wind_speed)
    TEST_GAUGE.labels('wind_gust').set(wind_gust)
    return 0

def poll_rain():
    rainfall = INTERRUPTS.get_rain(round_it=True)
    TEST_GAUGE.labels('rainfall').set(rainfall)
    return 0

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        # process_request(random.random())
        # LOGGING HERE?
        poll_bme()
        poll_temp()
        poll_rain()
        poll_wind()
        # print("Sleeping...")
        # time.sleep(GLOBAL_SLEEP)
