import requests
import os
import json
from backend.timeUtilities import RFC_1123_UTC_to_datetime
from datetime import datetime as dt
from datetime import timezone, timedelta
from pubsub import pub
import sqlite3


class WeatherAPI:
    def __init__(self) -> None:

        self.district = ""
        self.weather_settings = self.get_settings_from_JSON()
        self.expiration = self._set_expiration()
        self.headers = self._update_headers()
        self.url = self._set_url()

    def force_update(self):
        self.weather_settings = self.get_settings_from_JSON()
        self.expiration = self._set_expiration()
        self.headers = self._update_headers()
        self.url = self._set_url()

    def get_settings_from_JSON(self):
        print("WeatherAPI:")
        print("Loading settings from weather_settings.json")
        folder = os.path.join("backend",  "api_requests")
        filepath = os.path.join(folder, f"weather_settings.json")

        # Finds the saved district setting
        with open(filepath, "r") as file:
            data = json.load(file)
            print(" ")
            self.district: str = data.get("district").strip()
        print(f'selected district: {self.district}')
        filepath = os.path.join(folder, f"districts.sqlite3")
        statement = f"SELECT * FROM districts WHERE name = '{self.district}';"
        with DBConnectionManager(filepath) as db:
            db.cursor.execute(statement)
            data = db.cursor.fetchall()
            print(f'New settings: {data}')
            return {"lat": data[0][1], "lon": data[0][2], "last_modified": data[0][3], "expires": data[0][4]}

    def _update_headers(self):
        return {
            'User-Agent': "Aurinkoone by Mimirthful - github.com/mimirthful/aurinkoone-info-display",
            "If-Modified-Since": self.weather_settings.get("last_modified")
        }

    def _set_url(self):
        lat = self.weather_settings.get("lat")
        lon = self.weather_settings.get("lon")
        return f'https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={lat}&lon={lon}'

    def _set_setting(self, key, value):
        print("WeatherAPI:")
        print(f'Updating with {key}:{value}')
        folder = os.path.join("backend",  "api_requests")
        filepath = os.path.join(folder, f"districts.sqlite3")
        statement = f"UPDATE districts SET {key}='{value}' WHERE name='{self.district}';"
        print(statement)
        with DBConnectionManager(filepath) as db:
            db.cursor.execute(statement)
            db.connection.commit()
        self.weather_settings = self.get_settings_from_JSON()

    def _set_expiration(self, add_time=False):
        print("WeatherAPI:")
        print(
            f'Setting saved {self.weather_settings.get("expires")} as datetime')
        data = self.weather_settings
        timestamp = RFC_1123_UTC_to_datetime(
            data.get("expires"))  # type: ignore
        if add_time:
            print("Adding time to expiration due code 304")
            new = timestamp + timedelta(minutes=10)
            timestamp = new
        print("Weather info marked to expire at", timestamp)
        print(" ")
        return timestamp

    def fetch_weather(self):
        print("WeatherAPI:")
        print("--- Fetching Weather ---")
        present = dt.now(timezone.utc)
        if self.expiration < present:
            print("Timestamp has expired at ", self.expiration)
            print("Present time at ", present)
            response = requests.get(url=self.url, headers=self.headers)
            print(" ")
            print("Status", response.status_code)
            print(" ")
            if 'Expires' in response.headers:
                print(f"'Expires' found at response headers.")
                print(f"New expiration at ", response.headers['Expires'])
                self._set_setting("expires", response.headers['Expires'])
                if response.status_code == 304:
                    self.expiration = self._set_expiration(True)
                else:
                    self.expiration = self._set_expiration()
                print(" ")
            if 'Last-Modified' in response.headers:
                print(f"'Last-Modified' found at response headers.")
                self._set_setting(
                    "last_modified", response.headers['Last-Modified'])
                print(" ")

            if response.status_code == 200:
                print("Updating Weather.json file")
                try:
                    response_json = response.json()
                    json_str = json.dumps(response_json, indent=4)
                    weather_folder = os.path.join("backend",  "weather-JSON")
                    filepath = os.path.join(
                        weather_folder, f'weather_{self.district}.json')
                    with open(filepath, "w") as file:
                        file.write(json_str)
                    print("Update Succesful")
                    pub.sendMessage("New Weather data available")
                except Exception as error:
                    print("Update failed")
                    print(error)
            self.headers = self._update_headers()


class DBConnectionManager:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()  # type: ignore
