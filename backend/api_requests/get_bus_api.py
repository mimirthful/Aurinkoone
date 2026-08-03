import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime as dt
from datetime import timezone, timedelta


class BusAPI:
    def __init__(self) -> None:
        load_dotenv()
        self.key = os.getenv('digitransit-subscription-key')
        self.url = "https://api.digitransit.fi/routing/v2/waltti/gtfs/v1"
        self.expiration_dict = {}
        self.base_path = os.path.dirname(__file__)

    def delete_expiration_from_stop(self, name):
        try:
            self.expiration_dict.pop(f'tampere:{name}')
        except KeyError:
            print("No expiration key found")

    def get_stop_file(self, name):
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

        print("BusAPI: Fetching Bus", name)
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
