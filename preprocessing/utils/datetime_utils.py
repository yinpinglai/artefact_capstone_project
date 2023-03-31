import datetime

class DatetimeUtils:

    @classmethod
    def get_last_twelve_hours(cls):
        return datetime.datetime.now() - datetime.timedelta(hours=12)

    @classmethod
    def get_current_utc_time_str(cls):
        now = datetime.datetime.now(tz = datetime.timezone.utc)
        return now.strftime("%Y%m:%d_%H%M%S%z")
