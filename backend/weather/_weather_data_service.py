from datetime import datetime
from pubsub import pub
from ._weather_data_factory import WeatherObjectFactory as wof
from backend.timeUtilities import TimeManager


class WeatherDataService:
    def __init__(self):

        self._calendar = TimeManager()
        self._obj_maker = wof()
        self._obj_list = self._obj_maker.objects

        self.next_12_hours_per_hour = {
            "now": None,
            "1_hours_from_now": None,
            "2_hours_from_now": None,
            "3_hours_from_now": None,
            "4_hours_from_now": None,
            "5_hours_from_now": None,
            "6_hours_from_now": None,
            "7_hours_from_now": None,
            "8_hours_from_now": None,
            "9_hours_from_now": None,
            "10_hours_from_now": None,
            "11_hours_from_now": None,
        }
        self.next_7_days = {
            "today": None,
            "1_days_from_today": None,
            "2_days_from_today": None,
            "3_days_from_today": None,
            "4_days_from_today": None,
            "5_days_from_today": None,
            "6_days_from_today": None,
        }

        self.next_7_nights = {
            "tonight": None,
            "1_nights_from_today": None,
            "2_nights_from_today": None,
            "3_nights_from_today": None,
            "4_nights_from_today": None,
            "5_nights_from_today": None,
            "6_nights_from_today": None,
        }
        self._populate_lists()
        pub.subscribe(self.update, "New Weather data available")

    def update(self):
        self._obj_maker = wof()
        self._obj_list = self._obj_maker.objects
        self._populate_lists()

    def _get_obj_list_index(self, searched_date: datetime) -> int:
        data_array = self._obj_list

        left = 0
        right = len(data_array) - 1
        best_index = 0
        while left <= right:
            mid = left + (right - left) // 2

            time = self._calendar.compare_times_together(
                searched_date, self._obj_list[mid].datetime)

            # if index containing this date is found
            if not time.is_diff_date:
                # return if exact match
                if not time.is_diff_hour:
                    return mid
                if not time.is_in_future:
                    best_index = mid
                    left = mid + 1
                else:
                    right = mid - 1

            elif time.is_in_future:
                right = mid - 1

            else:
                left = mid + 1

        # date not on the list at all
        return best_index

    def _populate_lists(self):
        try:
            dict_length_12_hours = len(self.next_12_hours_per_hour)
            # returns next 12 hours datetimes
            time_arr = self._calendar.get_next_x_hours(dict_length_12_hours)
            i = 0
            for key in self.next_12_hours_per_hour:
                # Returns list index of an object at _obj_list with a datetime of time_arr[i]
                list_index = self._get_obj_list_index(time_arr[i])
                # picks said obj from the given list index
                obj = self._obj_list[list_index]
                # creates a list of next 12 hours temparatures
                obj.next_12_hours_temp = self._next_12_hours_temp(obj.datetime)
                # inserts obj as a var for the key on the dict
                self.next_12_hours_per_hour[key] = obj
                i = i + 1

            dict_length_7_days = len(self.next_7_days)
            time_arr = self._calendar.get_next_x_days(dict_length_7_days, 9)
            i = 0

            for key in self.next_7_days:
                obj = self._obj_list[self._get_obj_list_index(time_arr[i])]
                obj.next_12_hours_temp = self._next_12_hours_temp(obj.datetime)
                self.next_7_days[key] = obj
                i = i + 1

            dict_length_7_nights = len(self.next_7_nights)
            time_arr = self._calendar.get_next_x_days(dict_length_7_nights, 21)
            i = 0
            for key in self.next_7_nights:
                obj = self._obj_list[self._get_obj_list_index(time_arr[i])]
                obj.next_12_hours_temp = self._next_12_hours_temp(obj.datetime)
                self.next_7_nights[key] = obj
                i = i + 1
        except IndexError as e:
            print("WeatherDataService: No data on lists")

    def return_info_from_key(self, key: str) -> wof.WeatherData | None:
        if key in self.next_12_hours_per_hour:
            return self.next_12_hours_per_hour.get(key)
        if key in self.next_7_days:
            return self.next_7_days.get(key)
        if key in self.next_7_nights:
            return self.next_7_nights.get(key)

    def _next_12_hours_temp(self, start_time):
        # get datetimes as a list from next 12 hours starting from start_time
        time_arr = self._calendar.get_next_x_hours(12, start_time)
        temps = []
        i = 0
        while len(time_arr) > i:
            try:
                list_index = self._get_obj_list_index(time_arr[i])
                if list_index:
                    obj: wof.WeatherData = self._obj_list[list_index]

                    temps.append(obj.instant_air_temperature)

            except Exception as e:
                print(f'WeatherDataService: {e}')

            i = i + 1
        return temps
