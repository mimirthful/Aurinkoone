import datetime as dt
from datetime import timezone, timedelta
from backend.timeUtilities import TimeManager

tm = TimeManager()


def ISO_8601_to_datetime(time_str: str):
    """turns date formatted like "2026-06-17T17:28:18Z" into a datetime obj
    converts from UTC to local time, keeping only hour precision"""
    local_zone = dt.datetime.now().astimezone().tzinfo
    dt_obj = dt.datetime.fromisoformat(time_str.replace("Z", "+00:00"))
    dt_local = dt_obj.astimezone(local_zone)
    return dt_local.replace(minute=0, second=0, microsecond=0)


def RFC_1123_UTC_to_datetime(time: str):
    """for example '09 Jul 2026 07:11:06 GMT'"""
    format = '%a, %d %b %Y %H:%M:%S %Z'
    date = dt.datetime.strptime(time, format)
    return date.replace(tzinfo=timezone.utc)


def date_after_seconds(date: dt.datetime, seconds):
    midnight = date.replace(hour=0, minute=0, second=0)
    new = midnight + timedelta(seconds=seconds)
    return new


def UNIX_to_datetime(ts):
    return dt.datetime.fromtimestamp(ts)
