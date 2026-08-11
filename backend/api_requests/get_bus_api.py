import requests
import os
import json
from datetime import datetime as dt
from datetime import timezone, timedelta


class BusAPI:
    def __init__(self) -> None:
        self.url = "https://api.digitransit.fi/routing/v2/waltti/gtfs/v1"
        self.expiration_dict = {}
        self.base_path = os.path.dirname(__file__)
        self.key_path = os.path.join(self.base_path, f"bus_api_key.json")
        self.latest_date_path = os.path.join(
            self.base_path, f"bus_latest_response.json")
        self.key = self.get_api_key()
        self.latest_date = self.get_response_date()

    def remove_api_key(self):
        self.key = ""
        self.latest_date = ""
        os.remove(self.key_path)
        os.remove(self.latest_date_path)

    def get_response_date(self):
        try:
            with open(self.latest_date_path, "r") as file:
                data = json.load(file)
            return data.get("date")
        except FileNotFoundError:
            print(
                "BusAPI: Latest response date file not found, creating one.")
            with open(self.latest_date_path, 'x') as file:
                file.write('{"date": ""}')
                return ""

    def set_response_date(self, date):
        try:
            with open(self.latest_date_path, "w") as file:
                file.write(f'{{"date": "{date}"}}')
                self.latest_date = date
        except FileNotFoundError:
            print(
                "BusAPI: Latest response date file not found, creating one.")
            with open(self.latest_date_path, 'x') as file:
                file.write(f'{{"date":"{date}"}}')
                self.latest_date = date

    def save_api_key(self, key):
        try:
            with open(self.key_path, "w") as file:
                file.write(f'{{"key":"{key}"}}')
                self.key = key
        except FileNotFoundError:
            print(
                "BusAPI: API key file not found, creating one. Key must be set in the settings.")
            with open(self.key_path, 'x') as file:
                file.write(f'{{"key":"{key}"}}')
                self.key = key

    def get_api_key(self):
        try:
            with open(self.key_path, "r") as file:
                data = json.load(file)
            return data.get("key")
        except FileNotFoundError:
            print(
                "BusAPI: API key file not found, creating one. Key must be set in the settings.")
            with open(self.key_path, 'x') as file:
                file.write('{"key": ""}')
            return False

    def delete_expiration_from_stop(self, name):
        try:
            self.expiration_dict.pop(f'tampere:{name}')
        except KeyError:
            print("No expiration key found")

    def get_stop_file(self, name):
        if not self.get_api_key:
            return False
        is_valid = False
        body = """
        query($stopId: String!) {
            stop(id: $stopId) {
                code
                name(language: "string")
                stoptimesWithoutPatterns(numberOfDepartures: 12, omitCanceled: true) {
                    headsign
                    realtime
                    realtimeDeparture
                    scheduledDeparture
                    serviceDay
                    trip {
                        route {
                            color
                            longName
                            shortName
                            textColor
                        }
                    }
                }
            }
        }"""
        variables = {
            "stopId": name}
        print("BusAPI: Fetching bus", name)
        present = dt.now(timezone.utc)
        if name not in self.expiration_dict or self.expiration_dict[name] < present:
            print("BusAPI: Timestamp has expired")
            print("BusAPI: Present time at ", present)
            try:
                response = requests.post(url=self.url, json={"query": body, "variables": variables}, headers={
                    "Content-Type": "application/json", "digitransit-subscription-key": self.key})  # type: ignore
                if response.status_code == 200:
                    try:
                        is_valid = self.validate_response_data(response)
                        if is_valid:
                            self.set_response_date(
                                response.headers['Date'])
                            self.write_data_to_JSON(response, name, present)
                    except Exception as error:
                        print(error)
            except Exception:
                print("BusAPI: Could not fetch BusAPI data")
        else:
            print("BusAPI: Timestamp not expired yet, not fetching.")
            print("BusAPI: Timestamp expires at ", self.expiration_dict[name])
            print("BusAPI: Present at ", present)
        return is_valid

    def validate_response_data(self, response):
        response_json = response.json()
        stop = response_json.get("data").get("stop", {})
        if stop is None:
            return False
        return True

    def write_data_to_JSON(self, response, name, present):
        response_json = response.json()
        json_str = json.dumps(response_json, indent=4)
        json_folder_raw = os.path.join(self.base_path, "..",  "stops-JSON")
        json_folder = os.path.normpath(json_folder_raw)
        filepath = os.path.join(json_folder, f"{name}.json")
        self.expiration_dict[name] = present + \
            timedelta(minutes=7)
        print(
            f'BusAPI: new expiration for {name} at ', self.expiration_dict[name])
        with open(filepath, "w") as f:
            f.write(json_str)

    def set_api_key(self, key):
        name = "tampere:0002"
        body = """
        query($stopId: String!) {
            stop(id: $stopId) {
                code
        }"""
        variables = {
            "stopId": name}

        print("BusAPI: Testing API-key")

        response = requests.post(url=self.url, json={"query": body, "variables": variables}, headers={
            "Content-Type": "application/json", "digitransit-subscription-key": key})  # type: ignore
        if response.status_code == 200:
            print("BusAPI: Key is valid.")
            self.save_api_key(key)
            return True
        print("BusAPI: No internet connection or key is not valid.")
        return False
