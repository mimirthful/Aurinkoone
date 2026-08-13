import datetime as dt
import pytz
from .datetime_relation import DateTimeRelation


class TimeManager:
    def __init__(self):
        self._tz_zulu = pytz.timezone('Etc/Zulu')
        self._tz_home = pytz.timezone('Europe/Helsinki')

    def _get_time_now(self, timezone=None):
        time_now = dt.datetime.now()
        if timezone:
            return time_now.astimezone(timezone)
        return time_now

    def get_time_current(self):
        return self._get_time_now()

    def get_next_x_hours(self, hours: int, from_hours: dt.datetime | None = None) -> list[dt.datetime]:
        hours = hours - 1
        i = 0
        datetimes: list[dt.datetime] = []
        time = self._get_time_now()
        if from_hours:
            time = from_hours
        while i <= hours:
            res = time + dt.timedelta(hours=i)
            datetimes.append(res)
            i = i + 1
        return datetimes

    def get_next_x_days(self, days: int, from_hour: int = 00) -> list[dt.datetime]:
        i = 0
        datetimes: list[dt.datetime] = []
        time = self._get_time_now()
        while i <= days:
            fixed = time.replace(hour=from_hour)
            res = fixed + dt.timedelta(days=i)
            datetimes.append(res)
            i = i + 1
        return datetimes

    def compare_times_together(self, target: dt.datetime, comparable: dt.datetime) -> DateTimeRelation:
        """
        Returns object which contains info about the two dates relation to
        current time in UTC-0 
        """

        aware_comparable = comparable.astimezone(self._tz_zulu)
        aware_target = target.astimezone(self._tz_zulu)

        compared = DateTimeRelation(aware_target, aware_comparable)

        return compared
