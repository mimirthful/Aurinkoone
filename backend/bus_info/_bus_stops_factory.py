
from backend import read_json
from backend.timeUtilities import date_after_seconds, UNIX_to_datetime
import os


class BusStopsFactory:
    ''' This class reads .json files from the backend/JSON folder, \n
    and based on those files, creates BusStop objects. \n
    BusStop objects contain the bus stop's information and a list of StopTimes classes, \n
    which represent the singular busses arriving on the stop.'''

    def __init__(self):
        self.bus_stop_objects: list = []
        self.base_path = os.path.dirname(__file__)
        self.files_raw_path = os.path.join(self.base_path, "..", "stops-JSON")
        self.files_path = os.path.normpath(self.files_raw_path)
        self.update()

    def update(self) -> None:
        self.bus_stop_objects.clear()
        self._set_stops()

    def _set_stops(self) -> None:
        """
        Search for json files on self.files_path and tries to make a BusStop object out of them
        """
        try:
            for file in os.listdir(self.files_path):
                if file.endswith(".json"):
                    self.add_new_stop(file)
        except FileNotFoundError:
            print("No stops-JSON folder found. Creating one.")
            os.makedirs(self.files_path)

    def add_new_stop(self, filename: str) -> None:
        """
        Create a BusStop object based on the filename, add it into self.bus_stop_objects list

        Args:
            filename (str): name of the JSON file
        """
        try:
            stop_info = read_json(filename, self.files_path)
            data = stop_info.get("data", {})  # type: ignore
            bus_stop_object = self.BusStop(data, filename)
            self.bus_stop_objects.append(bus_stop_object)
        except Exception as e:
            print(e)

    class BusStop:

        def __init__(self, stop_info, json_file) -> None:
            self.json_file_name = json_file.replace(".json", "")
            self._stop_info: str = stop_info
            self.name: str = self._set_name()
            self.code: str = self._set_code()
            self.stop_times: list[self.StopTime] = []  # type: ignore

            self._set_stop_times()

        def _set_name(self) -> str:
            match self._stop_info:
                case {"stop": {"name": name}}:
                    return name
                case _:
                    return "Name not found"

        def _set_code(self) -> str:
            match self._stop_info:
                case {"stop": {"code": code}}:
                    return code
                case _:
                    return "Stop code not found"

        def _set_stop_times(self) -> str:
            match self._stop_info:
                case {"stop": {"stoptimesWithoutPatterns": stoptimes}}:
                    for stoptime in stoptimes:
                        try:
                            object = self.StopTime(stoptime)
                            self.stop_times.append(object)
                        except:
                            print("_set_stop_times: couldn't create object")
                case _:
                    return "No stop info"

        def __str__(self) -> str:
            return f'{self.name} {self.code}'

        class StopTime:
            def __init__(self, stop_time: dict):
                self._info = stop_time
                self.service_day = self.get_service_day()
                self.scheduled_departure = self.to_datetime(self._info.get(
                    "scheduledDeparture", None))
                self.realtime_departure = self.to_datetime(self._info.get(
                    "realtimeDeparture", None))
                self.realtime: bool = self._info.get(
                    "realtime", False)
                self.headsign = self._info.get("headsign", None)

                self.short_name = self._info.get("trip", {}).get(
                    "route", {}).get("shortName", "None")
                self.long_name = self._info.get("trip", {}).get(
                    "route", {}).get("longName", "None")
                self.color = self._info.get("trip", {}).get(
                    "route", {}).get("color", "000000")
                self.text_color = self._info.get("trip", {}).get(
                    "route", {}).get("textColor", "ffffff")

            def get_service_day(self):
                unix = self._info.get("serviceDay", 0)
                to_date = UNIX_to_datetime(unix)
                return to_date

            def to_datetime(self, time_tag):
                time = None
                if time_tag is not None:
                    try:
                        time = date_after_seconds(self.service_day, time_tag)
                    except Exception as e:
                        print(e)
                return time

            def __str__(self) -> str:
                return f'{self.short_name} {self.long_name}'
