import wx
from pubsub import pub
from gui import FrontFrame
from model import Model


class Controller:
    def __init__(self):
        self.model = Model()
        pub.subscribe(self.model.start_threads, "ui_ready")
        pub.subscribe(self.update_frames, "threads_started")

        pub.subscribe(self.update_frames, "weather_updated")
        pub.subscribe(self.clear_content, "stops_updated")
        pub.subscribe(self.create_bus_stops, "notebook_bus_panel_empty")
        pub.subscribe(self.OnClose, "closing")
        # Bus stop  and weather settings subcriptions
        pub.subscribe(self.create_new_bus_stop, "new_stop")
        pub.subscribe(self.delete_bus_stop, "delete_stop")
        pub.subscribe(self.update_weather_setting, "weather_area_changed")
        pub.subscribe(self.get_latest_response_date, "stops_updated")
        # API key settings subcriptions
        pub.subscribe(self.check_api_key_status, "api_key_status_check")
        pub.subscribe(self.set_api_key, "api_key_added")
        pub.subscribe(self.remove_api_key, "api_key_removed")

        self.main_frame = FrontFrame("Aurinkoone")
        self.main_frame.Show()

    def update_frames(self):
        self.get_district_name()
        self.update_hourly_forecast()
        self.update_daily_forecast()
        self.update_uv()
        self.update_rain()
        self.update_wind()
        self.return_stop_list_codes()

    def OnClose(self):
        self.model.is_updating = False
        pub.unsubAll()
        self.main_frame.Destroy()
        print("Exit")

# -------------------------- BUS STOPS -------------------------
    # --- API KEY ---

    def remove_api_key(self):
        stop_list = self.model.return_stop_list_codes()
        for stop in stop_list:
            self.delete_bus_stop(stop)

        self.model.remove_api_key()
        wx.CallAfter(pub.sendMessage,
                     "latest_response_date_changed", date="")
        wx.CallAfter(pub.sendMessage,
                     "api_key_info_changed", key_exists=False)

    def get_latest_response_date(self):
        date = self.model.get_latest_response_date()
        wx.CallAfter(pub.sendMessage,
                     "latest_response_date_changed", date=date)

    def set_api_key(self, key):
        valid = True
        stripped = key.strip()
        message = "API key is either not valid\nor there is no internet connection."
        previous_key = self.model.get_api_key()

        if stripped == previous_key:
            message = "Given key is already set. No need to reset."
            valid = False

        if valid:
            success = self.model.set_api_key(stripped)
            if success:
                message = "API key set succesfully."
                wx.CallAfter(pub.sendMessage,
                             "api_key_info_changed", key_exists=True)

        wx.CallAfter(pub.sendMessage,
                     "api_key_changed_status_response", message=message)

    def check_api_key_status(self):
        is_key = self.model.check_api_key_status()
        wx.CallAfter(pub.sendMessage, "api_key_info_changed",
                     key_exists=is_key)

    # --- STOPS ---

    def return_stop_list_codes(self):
        list = self.model.return_stop_list_codes()
        wx.CallAfter(pub.sendMessage, "stop_list_codes", codes=list)

    def clear_content(self):
        wx.CallAfter(pub.sendMessage, "clear_notebook_bus_panel")

    def delete_bus_stop(self, stop_code):
        self.model.delete_bus_stop(stop_code)
        self.return_stop_list_codes()

    def create_new_bus_stop(self, stop_code):
        message = self.model.add_bus_stop(stop_code)
        wx.CallAfter(pub.sendMessage, "bus_stop_created_message",
                     message=message)
        self.return_stop_list_codes()

    def create_bus_stops(self):
        stops = self.model.get_all_stops_readable()
        for stop in stops:
            wx.CallAfter(pub.sendMessage, "stop_available", data=stop)

# -------------------------- WEATHER ---------------------------
    def update_weather_setting(self, district):
        self.model.update_weather_setting_JSON(district)
        self.model.force_update_weather()

    def get_district_name(self):
        name = self.model.get_district_name()
        wx.CallAfter(pub.sendMessage, "district_name_available", district=name)

    def update_uv(self):
        data = self.model.get_UV()
        wx.CallAfter(pub.sendMessage, "uv", data=data)

    def update_wind(self):
        data = self.model.get_wind_speed()
        wx.CallAfter(pub.sendMessage, "wind", data=data)

    def update_rain(self):
        data = self.model.get_rain_change("now")
        wx.CallAfter(pub.sendMessage, "rain", data=data)

    def update_hourly_forecast(self):
        parent_topic = pub.getDefaultTopicMgr().getTopic("hourly_forecast")
        subtopics = parent_topic.getSubtopics()

        for topic in subtopics:
            name = topic.getName()
            short_name = self.get_short_name(name)
            data = self.model.get_temperature(short_name)
            rain_change = self.model.get_rain_change(short_name)
            rain_label = f'🌢 {rain_change.get("info_label")}'
            data["rain_change"] = rain_label
            wx.CallAfter(pub.sendMessage, name, data=data)

        wx.CallAfter(pub.sendMessage, "hourlyforecastpanel_updated")

    def update_daily_forecast(self):
        parent_topic = pub.getDefaultTopicMgr().getTopic("daily_forecast")
        subtopics = parent_topic.getSubtopics()

        for topic in subtopics:
            name = topic.getName()
            short_name = self.get_short_name(name)
            data = self.model.get_24_forecast(int(short_name))
            wx.CallAfter(pub.sendMessage, name, data=data)

    def get_short_name(self, full_name):
        return full_name.split('.')[-1]
