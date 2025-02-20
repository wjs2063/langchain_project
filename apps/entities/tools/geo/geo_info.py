from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter
from langchain_core.tools import Tool, tool

# locator = Nominatim(user_agent="geo_info", adapter_factory=AioHTTPAdapter)
locator = Nominatim(user_agent="geo_info")


@tool
def fetch_coordination_tool(location) -> dict[str, str]:
    """
    특정지역의 위도,경도를 반환합니다
    """
    response = locator.geocode(location)
    return {"lat": response["latitude"], "lon": response["longitude"]}


# print(locator.geocode("서울 천호동").raw)
