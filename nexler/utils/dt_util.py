from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_current_time():
    """Return the current time"""
    return datetime.now()


def format_date(date, format_str='%Y-%m-%d'):
    """Return the given datetime object as a string in the given format."""
    return date.strftime(format_str)


def human_date(date, format_str='%d/%m/%Y'):
    """Return the given datetime object as a string in the given format."""
    return date.strftime(format_str)


def parse_date(date_str, format_strs=None):
    """Return a datetime object from the given string, trying each of the given formats."""
    if format_strs is None:
        format_strs = ['%Y-%m-%d', '%d/%m/%Y']
    for format_str in format_strs:
        try:
            return datetime.strptime(date_str, format_str)
        except ValueError:
            continue
    raise ValueError(f"No valid date format found for {date_str}")


def add_days(date, days):
    """Return a datetime that is the given number of days after the given date."""
    return date + relativedelta(days=+days)


def add_hours(date, hours):
    """Return a datetime that is the given number of hours after the given date."""
    return date + relativedelta(hours=+hours)


def add_minutes(date, minutes):
    """Return a datetime that is the given number of minutes after the given date."""
    return date + relativedelta(minutes=+minutes)


def add_years(date, years):
    """Return a datetime that is the given number of years after the given date."""
    return date + relativedelta(years=+years)


def time_difference(date1, date2):
    """Return the difference between two datetime objects as a timedelta."""
    date1, date2 = ensure_datetime(date1, date2)
    return date2 - date1


def days_difference(date1, date2):
    """Return the difference between two datetime objects in days."""
    date1, date2 = ensure_datetime(date1, date2)
    return (date2 - date1).days


def hours_difference(date1, date2):
    """Return the difference between two datetime objects in hours."""
    date1, date2 = ensure_datetime(date1, date2)
    return ((date2 - date1).seconds // 3600) + (date2 - date1).days * 24


def minutes_difference(date1, date2):
    """Return the difference between two datetime objects in minutes."""
    date1, date2 = ensure_datetime(date1, date2)
    return ((date2 - date1).seconds // 60) + (date2 - date1).days * 24 * 60


def ensure_datetime(date1, date2):
    """Ensure the inputs are datetime objects, parsing them if necessary."""
    if isinstance(date1, str):
        date1 = parse_date(date1)
    if isinstance(date2, str):
        date2 = parse_date(date2)
    return date1, date2
