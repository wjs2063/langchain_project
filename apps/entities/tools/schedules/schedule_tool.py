from langchain_core.tools import Tool, tool
from apps.entities.tools.schedules.google_calendar import get_google_calendar_events
from datetime import datetime, timezone
import pytz

"""
사용자가 3일전 일정을 알려달라는경우 어디까지의 범위로 알려줘야 하는걸까 
사용자가 3일후 오전일정 알려달라는경우 어디까지의 범위?
"""


@tool
def get_my_schedule(interval: int = 1):
    """
    현재 시각을 기준으로 사용자가 원하는 범위의 스케쥴을 가져옵니다. interval := 사용자가 원하는 일정범위
    """
    time_zone = pytz.timezone("Asia/Seoul")
    current_time = datetime.now(time_zone)
    return get_google_calendar_events(time_min=current_time, interval=interval)


# time_zone = pytz.timezone("Asia/Seoul")
# current_time = datetime.now(time_zone)
# fetch_my_schedule.invoke({"time_min": current_time, "interval": 1})
