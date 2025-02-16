from langchain_core.tools import Tool, tool, StructuredTool
from datetime import datetime
from pydantic import BaseModel


@tool
def get_current_date(text: str) -> str:
    """
    Returns current time in 현재 날짜 : XXXX년 XX월 XX일 XX시 XX분
    """
    _now = datetime.now()
    return f"현재 날짜 : {_now.year}년 {_now.month}월 {_now.day}일 {_now.hour}시 {_now.minute}분"


current_time_tool = Tool(
    func=get_current_date,
    name="Time",
    description="현재 시간을 반환합니다.",
    # return_type=TimeOutput,
    # return_direct=True,
    # args_schema=EmptyInput,  # 입력을 필요로 하지 않는 구조체 사용
)
