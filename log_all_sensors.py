#!/usr/bin/python3
import interrupt_client
import ds18b20_therm
import bme280_sensor
import wind_direction_byo
import database 

# Set-up weather objects
wind_dir = wind_direction_byo
interrupts = interrupt_client.interrupt_client(port = 49501)
db = database.weather_database() # Local sqlite3 databse

wind_average = round(wind_dir.get_value(10), 2) # ten seconds

temp_probe = ds18b20_therm.DS18B20()
humidity, pressure, ambient_temp = bme280_sensor.read_all()

print("Inserting...")
db.insert(ambient_temp, temp_probe.read_temp(), 0.0, pressure, humidity, wind_average, interrupts.get_wind(round_it=True), interrupts.get_wind_gust(round_it=True), interrupts.get_rain(round_it=True))
print("done")

interrupts.reset()
