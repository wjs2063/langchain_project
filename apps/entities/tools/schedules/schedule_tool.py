from langchain_core.tools import Tool, tool
from apps.entities.tools.schedules.google_calendar import fetch_google_calendar_events
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


# time_zone = pytz.timezone("Asia/Seoul")
# current_time = datetime.now(time_zone)
# fetch_my_schedule.invoke({"time_min": current_time, "interval": 1})
