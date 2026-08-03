import time
import os
import json
import threading
from pubsub import pub
from backend.api_requests import BusAPI
from backend.api_requests import WeatherAPI
import backend.weather
import backend.bus_info


class Model:
    def __init__(self):
        # Handable data
        self.bus_service = backend.bus_info.BusStopService()
        self.weather_service = backend.weather.WeatherDataService()
        # Api fetchers
        self.weather_api = WeatherAPI()
        self.bus_api = BusAPI()
        # Starting the updater threads
        self.is_updating = True

    def start_threads(self):
        self.update_weather_thread = threading.Thread(
            target=self.update_weather, daemon=True)
        self.update_stops_thread = threading.Thread(
            target=self.update_stops, daemon=True)
        self.update_stops_thread.start()
        self.update_weather_thread.start()

        pub.sendMessage("threads_started")

    def force_update_bus(self):
        self.bus_service.refresh_stop_list()
        bus_stops = self.bus_service.stop_list
        if len(bus_stops) > 0:
            for stop in bus_stops:
                self.bus_api.get_stop_file(stop.json_file_name)
        pub.sendMessage("stops updated")

    def force_update_weather(self):
        self.weather_api.force_update()
        self.weather_api.fetch_weather()
        pub.sendMessage("New Weather data available")
        pub.sendMessage("weather updated")

# -------------------------- THREADS ---------------------------

    def update_weather(self):
        while self.is_updating:
            self.weather_api.fetch_weather()
            pub.sendMessage("weather updated")
            time.sleep(120)

    def update_stops(self):
        while self.is_updating:
            self.bus_service.refresh_stop_list()
            bus_stops = self.bus_service.stop_list
            if len(bus_stops) > 0:
                for stop in bus_stops:
                    self.bus_api.get_stop_file(stop.json_file_name)
            pub.sendMessage("stops updated")
            time.sleep(180)

# -------------------------- BUS STOPS -------------------------
    def return_stop_list_codes(self) -> list[str]:
        return self.bus_service.return_stop_list_codes()

    def add_bus_stop(self, stop_code):
        '''
            Fetch a bus stop with given stop_code, and add stop to the lists. \n
            If success, send a "new stop added" message
        '''
        if not stop_code.isdigit():
            return "The code must only have numbers."
        if not len(stop_code) == 4:
            return "The code must be four numbers long."
        filename = f'{stop_code}'
        try:
            added = self.bus_api.get_stop_file(filename)
            if added:
                self.bus_service.add_stop(filename)
                pub.sendMessage("stops updated")
                return f'Stop [{stop_code}] added.'
            return f'Stop [{stop_code}] not found on backend or already exists.'
        except Exception as e:
            print(e)

    def delete_bus_stop(self, stop_code):
        stop_object = self.find_stop_by_code(stop_code)
        if stop_object:
            self.bus_api.delete_expiration_from_stop(stop_code)
            self.bus_service.delete_stop(stop_object)
            pub.sendMessage("stops updated")

    def find_stop_by_code(self, stop_code):
        stop_object = None
        for item in self.bus_service.stop_list:
            if int(item.code) == int(stop_code):
                stop_object = item
                break
        return stop_object

    def get_single_stop_readable(self, stop):
        stop_dict = {}
        stop_dict["name"] = stop.name
        stop_dict["code"] = stop.code
        stop_dict["stop_times"] = []

        for bus in stop.stop_times:
            bus_info = {}
            bus_info["bus_short_name"] = bus.short_name
            bus_info["headsign"] = bus.headsign
            bus_info["realtime"] = bus.realtime
            bus_info["bus_real_time_dep"] = bus.realtime_departure
            bus_info["bus_scheduled_dep"] = bus.scheduled_departure
            bus_info["bus_color"] = bus.color
            bus_info["bus_text_color"] = bus.text_color
            stop_dict["stop_times"].append(bus_info)
        return stop_dict

    def get_all_stops_readable(self):
        '''
        Return a dictionary containing all bus stops info in a presentable way
        '''
        bus_stop_list = []
        stops = self.bus_service.stop_list
        for stop in stops:
            stop_dict = self.get_single_stop_readable(stop)
            bus_stop_list.append(stop_dict)
        return bus_stop_list

# -------------------------- WEATHER ---------------------------
    def get_district_name(self):
        base_path = os.path.dirname(__file__)
        folder = os.path.join(base_path, "backend",  "api_requests")
        filepath = os.path.join(folder, f"weather_settings.json")
        # Finds the saved district setting
        with open(filepath, "r") as file:
            data = json.load(file)
        return data.get("district")

    def update_weather_setting_JSON(self, district):
        base_path = os.path.dirname(__file__)
        folder = os.path.join(base_path, "backend",  "api_requests")
        filepath = os.path.join(folder, f"weather_settings.json")
        d = {"district": district}
        # Finds the saved district setting
        with open(filepath, "w") as file:
            json.dump(d, file)

    def get_area(self):
        return self.weather_api.district

    def get_temperature(self, key: str, hours: int = 1):
        placeholder_img = os.path.join(
            "icons_weather", f'icons8-full-image-100.png')
        obj = self.weather_service.return_info_from_key(key)
        if obj:
            temp = obj.instant_air_temperature
            icon = None
            hour = obj.datetime.hour

            weekday: str = obj.weekday
            match hours:
                case 1:
                    icon = obj.next_1_hours_symbol_path
                case 6:
                    icon = obj.next_6_hours_symbol_path
                case 12:
                    icon = obj.next_12_hours_symbol_path

            return {"image": icon, "label": f'{temp}°C', "hour": str(hour), "weekday": weekday}
        return {"image": placeholder_img, "label": "0°C", "hour": "00", "weekday": "Loading"}

    def get_UV(self) -> dict:
        obj = self.weather_service.return_info_from_key("now")
        if obj:
            uv = obj.instant_ultraviolet_index_clear_sky
            return {"info_name": "UV", "info_label": f'{str(uv)}'}
        return {}

    def get_wind_speed(self) -> dict:
        obj = self.weather_service.return_info_from_key("now")
        if obj:
            wind_speed = obj.instant_wind_speed
            if wind_speed:
                return {"info_name": "Wind speed", "info_label": f'{str(int(wind_speed))}km/h'}
        return {}

    def get_rain_change(self, key, hours: int = 1) -> dict:

        obj = self.weather_service.return_info_from_key(key)
        if obj:
            rain_change = obj.next_1_hours_rain_change
            if rain_change:
                return {"info_name": "Rain change", "info_label": f'{str(rain_change)}%'}
        return {"info_name": "Rain change", "info_label": f'00%'}

    def get_24_forecast(self, days_from_today: int) -> dict[str, str]:
        placeholder_img = os.path.join(
            "icons_weather", f'icons8-full-image-100.png')
        day_str = "today"
        night_str = "tonight"
        if days_from_today != 0:
            day_str = f'{days_from_today}_days_from_today'
            night_str = f'{days_from_today}_nights_from_today'

        needed_info = {"weekday": "Loading...", "rain_change": "0%",
                       "image_day": placeholder_img, "image_night": placeholder_img,
                       "temperature_day": "0°C",
                       "temperature_night": "0°C"}

        day = self.weather_service.return_info_from_key(day_str)
        night = self.weather_service.return_info_from_key(night_str)
        if day and night:
            daytemp = -999
            for item in day.next_12_hours_temp:
                if item > daytemp:
                    daytemp = item

            nighttemp = 999
            for item in night.next_12_hours_temp:
                if item < nighttemp:
                    nighttemp = item

            needed_info["weekday"] = day.weekday
            if days_from_today == 0:
                needed_info["weekday"] = "Today"
            needed_info["image_day"] = day.next_12_hours_symbol_path
            night_symbol_path = night.next_12_hours_symbol_path
            night = night_symbol_path.replace("day", "night")
            needed_info["image_night"] = night
            needed_info["temperature_day"] = f'{daytemp}°C'
            needed_info["temperature_night"] = f'{nighttemp}°C'

        return needed_info
