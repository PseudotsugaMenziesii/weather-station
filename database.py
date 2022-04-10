#!/usr/bin/python3
import sqlite3 # MySQLdb 
import datetime, http.client, json, os
import io
import gzip


class sqlite_database:
    def __init__(self):
        self.connection = sqlite3.connect('/home/pi/weather_private/weather.db')
        self.cursor = self.connection.cursor()

    def execute(self, query, params = []):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except:
            self.connection.rollback()
            raise

    def query(self, query):
        cursor = self.connection.cursor(sqlite3.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()

class weather_database:
    def __init__(self):
        self.db = sqlite_database()
        self.insert_template = "INSERT INTO WEATHER_MEASUREMENT (AMBIENT_TEMPERATURE, GROUND_TEMPERATURE, AIR_QUALITY, AIR_PRESSURE, HUMIDITY, WIND_DIRECTION, WIND_SPEED, WIND_GUST_SPEED, RAINFALL) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.update_template =  "UPDATE WEATHER_MEASUREMENT SET REMOTE_ID=%s WHERE ID=%s;"
        self.upload_select_template = "SELECT * FROM WEATHER_MEASUREMENT WHERE REMOTE_ID IS NULL;"

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_none(self, val):
        return val if val != None else "NULL"

    def insert(self, ambient_temperature, ground_temperature, air_quality, air_pressure, humidity, wind_direction, wind_speed, wind_gust_speed, rainfall):
        params = (ambient_temperature,
            ground_temperature,
            air_quality,
            air_pressure,
            humidity,
            wind_direction,
            wind_speed,
            wind_gust_speed,
            rainfall)
        print(f"{self.insert_template} {params};")
        self.db.execute(self.insert_template, params)
