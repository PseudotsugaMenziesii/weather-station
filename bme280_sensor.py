import bme280
import smbus2
from time import sleep

port = 1 # default is 1
address = 0x77 # Adafruit BME280 address (0x77). Other BME280s may be different
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

def read_all():
    bme280_data = bme280.sample(bus,address)
    return round(bme280_data.humidity, 2), round(bme280_data.pressure, 2), round(bme280_data.temperature, 2)

if __name__ == '__main__':
    print(read_all())