# `dt_util.py` User Documentation

The `dt_util.py` module provides a set of utility functions for date and time manipulation. This makes it easy for your application to perform common operations such as formatting date strings, calculating date differences, and adding time intervals to dates.

## Functions

- **get_current_time()**: This function returns the current datetime object.

- **format_date(date, format_str='%Y-%m-%d')**: This function formats a given date as per the specified format string.

- **human_date(date, format_str='%d/%m/%Y')**: This function returns a human-readable date string of the provided date object.

- **parse_date(date_str, format_strs=None)**: This function returns a datetime object parsed from the given string.

- **add_days(date, days)**, **add_hours(date, hours)**, **add_minutes(date, minutes)**, **add_years(date, years)**: These functions return a datetime object that represents the given date plus the specified number of days, hours, minutes, or years.

- **time_difference(date1, date2)**, **days_difference(date1, date2)**, **hours_difference(date1, date2)**, **minutes_difference(date1, date2)**: These functions return the difference between two datetime objects as a `timedelta` object, or in days, hours, or minutes.

- **ensure_datetime(date1, date2)**: This function ensures that `date1` and `date2` are `datetime` objects, parsing them if necessary.

## Usage

To use these utility functions, import the required functions from the `dt_util` module and use them in your code where needed. 

For example:

```python
from nexler.utils.dt_util import add_days, days_difference, get_current_time


def schedule_meeting():
    meeting_date = add_days(get_current_time(), 3)
    # ... other scheduling code ...


def get_meeting_duration(meeting_start, meeting_end):
    duration = days_difference(meeting_start, meeting_end)
    return duration
```

In this example, the `add_days` function is used to schedule a meeting three days from the current date, and the `days_difference` function is used to calculate the duration of a meeting in days.