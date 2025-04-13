from langchain_core.tools import Tool, tool
from apps.entities.tools.schedules.google_calendar import (
    fetch_google_calendar_events,
    insert_google_calendar_events,
)
from datetime import datetime, timezone
import pytz

"""
사용자가 3일전 일정을 알려달라는경우 어디까지의 범위로 알려줘야 하는걸까 
사용자가 3일후 오전일정 알려달라는경우 어디까지의 범위?
"""


@tool
def fetch_my_schedule(interval: int = 1):
    """
    현재 시각을 기준으로 사용자가 원하는 범위의 스케쥴을 가져옵니다. interval := 사용자가 원하는 일정범위
    3일전이라면 interval = -3
    2일전이라면 interval = -2
    1일전이라면 interval = -1
    오늘이라면 interval = +0
    내일이라면 interval = +1
    """
    time_zone = pytz.timezone("Asia/Seoul")
    current_time = datetime.now(time_zone)
    return fetch_google_calendar_events(current_time=current_time, interval=interval)


@tool
def add_my_schedule(
    summary: str, description: str, requested_start_time: datetime, interval: int = 30
):
    """
    Adds an event to a Google Calendar.

    This function schedules a new event on a Google Calendar. It utilizes the
    `insert_google_calendar_events` function to handle the actual insertion of
    events into the calendar. The event consists of a summary, description,
    start time, and a default interval duration.

    Arguments:
        summary: str
            The title or summary of the event.
        description: str
            Additional details or description of the event.
        requested_start_time: datetime
            The desired start time for the event.
        interval: int, optional
            The duration of the event in minutes. Defaults to 30.

    Returns:
        Depends on the return of `insert_google_calendar_events`. Typically,
        returns a representation of the created event, or confirmation of
        successful addition.
    """
    return insert_google_calendar_events(
        summary=summary,
        description=description,
        requested_start_time=requested_start_time,
        interval=30,
    )


# time_zone = pytz.timezone("Asia/Seoul")
# current_time = datetime.now(time_zone)
# fetch_my_schedule.invoke({"time_min": current_time, "interval": 1})
