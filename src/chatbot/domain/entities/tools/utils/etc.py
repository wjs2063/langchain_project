from datetime import datetime

from langchain_core.tools import StructuredTool, Tool, tool
from pydantic import BaseModel


@tool
def current_date_tool(text: str) -> str:
    """
    Returns current time in 현재 날짜 : XXXX년 XX월 XX일 XX시 XX분
    """
    _now = datetime.now()
    return f"현재 날짜 : {_now.year}년 {_now.month}월 {_now.day}일 {_now.hour}시 {_now.minute}분"


