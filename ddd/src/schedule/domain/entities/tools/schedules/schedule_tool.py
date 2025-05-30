from langchain_core.tools import Tool, tool
from apps.entities.tools.schedules.google_calendar import (
    fetch_google_calendar_events,
    add_google_calendar_events,
)
from datetime import datetime, timezone
import pytz

"""
사용자가 3일전 일정을 알려달라는경우 어디까지의 범위로 알려줘야 하는걸까 
사용자가 3일후 오전일정 알려달라는경우 어디까지의 범위?
"""
time_zone = pytz.timezone("Asia/Seoul")


@tool
def fetch_my_schedule(interval: int = 1):
    """
    Fetches the user's schedule from Google Calendar within the specified interval
    using their current local time in the 'Asia/Seoul' timezone. This function
    retrieves events starting from the current time up to the specified number
    of days ahead. The events are fetched specifically for the authenticated
    Google Calendar user.

    Args:
        interval (int): The number of days starting from the current day for
        which the calendar events should be fetched. Defaults to 1.

    Returns:
        List[dict]: A list of events where each event is represented as
        a dictionary containing event details.
    """
    time_zone = pytz.timezone("Asia/Seoul")
    current_time = datetime.now(time_zone)
    return fetch_google_calendar_events(current_time=current_time, interval=interval)


@tool
def add_my_schedule(
    summary: str,
    description: str,
    requested_start_time: datetime = datetime.now(time_zone),
    interval: int = 30,
):
    """
    Adds a schedule to the Google Calendar by creating an event with specified information.

    This function facilitates the insertion of an event into the Google Calendar
    using the provided details such as its summary, description, start time, and
    interval. It leverages the `insert_google_calendar_events` function for event
    creation.

    Parameters:
        summary (str): The title or summary of the event to add to the calendar.
        description (str): A detailed description of the event being created.
        requested_start_time (datetime): The start time of the event. Defaults to the
            current datetime in the specified time zone if not provided.
        interval (int): The duration of the event in minutes. Defaults to 30.

    Returns:
        The return value of `insert_google_calendar_events`, which could represent the
        result or response from the Google Calendar API upon successful event creation.
    """
    return add_google_calendar_events(
        summary=summary,
        description=description,
        requested_start_time=requested_start_time,
        interval=interval,
    )


# time_zone = pytz.timezone("Asia/Seoul")
# current_time = datetime.now(time_zone)
# fetch_my_schedule.invoke({"time_min": current_time, "interval": 1})
