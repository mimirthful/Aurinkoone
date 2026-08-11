from backend import read_json
import os
from backend.timeUtilities import ISO_8601_to_datetime
import calendar
import json


class WeatherObjectFactory:
    def __init__(self):
        self.district = self.get_district_name()
        self._info = self._set_info()
        self._timeseries_list = self._set_timeseries_list()
        self._datestring_to_datetime = ISO_8601_to_datetime
        self.objects = []
        self._create_from_all_spots()

# setters
    def get_district_name(self):

        base_path = os.path.dirname(__file__)
        folder = os.path.join(base_path, "..", "api_requests")
        filepath = os.path.join(folder, f"weather_settings.json")
        filepath = os.path.normpath(filepath)
        folder = os.path.normpath(folder)
        # Finds the saved district setting
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
            return data.get("district")
        except FileNotFoundError:
            print(
                "WeatherObjectFactory: No weather_settings.json file found. Creating one.")
            with open(filepath, 'x') as file:
                file.write('{"district": "Finlayson"}')
            self.get_district_name()

    def _set_info(self):
        self.get_district_name()
        try:
            base_path = os.path.dirname(__file__)
            folder = os.path.join(base_path, "..", "weather-JSON")
            filepath = os.path.normpath(folder)
            data = read_json(f'weather_{self.district}', filepath)
            return data
        except Exception as e:
            print("WeatherObjectFactory: No weather info yet")
        return {"info": None}

    def _set_timeseries_list(self) -> list | None:
        try:
            if self._info:
                timeseries_list = self._info.get(
                    "properties", {}).get("timeseries", [])  # type: ignore
                return timeseries_list
        # if timeseries list is empty
        except IndexError as error:
            print(f'WeatherObjectFactory: {error} is empty')
            return []
        except AttributeError as error:
            print("WeatherObjectFactory: Attribute error ", error)
            return []

    class WeatherData:
        def __init__(self, info_dict: dict):
            self._info_dict = info_dict
            self._datestring_to_datetime = ISO_8601_to_datetime
            self.datetime = self._set_datetime()
            self.weekday = calendar.day_name[self.datetime.weekday()]
            self.instant_air_temperature = self._get_instant_detail(
                "air_temperature")
            self.instant_relative_humidity = self._get_instant_detail(
                "relative_humidity")
            self.instant_wind_from_direction = self._get_instant_detail(
                "wind_from_direction")
            self.instant_ultraviolet_index_clear_sky = self._get_instant_detail(
                "ultraviolet_index_clear_sky")
            self.instant_wind_speed = self._get_instant_detail("wind_speed")

            self.next_1_hours_rain_change = self._get_x_hours_details(
                1, "probability_of_precipitation")

            self.next_12_hours_symbol_path = self._find_weather_icon(12)
            self.next_12_hours_temp = []
            self.next_1_hours_symbol_path = self._find_weather_icon(1)
            self.next_6_hours_symbol_path = self._find_weather_icon(6)

        def _set_datetime(self):
            time = self._info_dict.get("time", None)
            if time:
                datetime_obj = self._datestring_to_datetime(time)
                return datetime_obj
            raise ValueError("WeatherData: Could not determine timestamp")

        # get 1/6/12 h icons
        def _get_icon_code(self, next_hours):
            hours_str = f'next_{next_hours}_hours'
            try:
                symbol = self._info_dict.get("data", {}).get(
                    hours_str, {}).get("summary", {}).get("symbol_code")
                return symbol

            except AttributeError as error:
                print(f'WeatherData: _get_icon_code():{error}')
                return None

        def _find_weather_icon(self, next_hours):
            name = self._get_icon_code(next_hours)
            base_path = os.path.dirname(__file__)
            if name:

                path = os.path.join(base_path, "..", "..",
                                    "icons_weather", f'{name}.png')
                normalized = os.path.normpath(path)
                return normalized
            path = os.path.join(base_path, "..", "..",
                                "icons_weather", f'icons8-full-image-100.png')
            return os.path.normpath(path)

        def _get_instant_detail(self, requested_detail):
            match self._info_dict:
                case {"data": {"instant": {"details": details_dict}}}:
                    if requested_detail in details_dict:
                        return details_dict.get(requested_detail)
                case _:
                    return None

        def _get_x_hours_details(self, next_hours, requested_detail) -> int | str | None:
            hours_str = f'next_{next_hours}_hours'
            try:
                detail = self._info_dict.get("data", {}).get(
                    hours_str, {}).get("details", {}).get(requested_detail)
                return detail
            except:
                return None

    def _create_info_obj(self, list_spot):
        try:
            info_obj = self.WeatherData(list_spot)
            return info_obj

        except Exception as error:
            print(f'WeatherData: _create_info_obj(): {error}')
            return None

    def _create_from_all_spots(self):
        if self._timeseries_list:
            for item in self._timeseries_list:
                obj = self._create_info_obj(item)
                self.objects.append(obj)
