import os

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

from apps.entities.tools.geo.geo_info import locator

load_dotenv()


@tool
def get_weather(location: str) -> str:
    """주어진 위치의 현재 날씨 정보를 조회합니다."""
    # API 키 설정
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    if not api_key:
        return "OpenWeatherMap API 키가 설정되지 않았습니다."

    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # 입력 전처리
    location = location.strip("'\"")

    try:
        response = locator.geocode(location)
        # API 요청 파라미터 설정
        params = {
            "lat": response.raw["lat"],
            "lon": response.raw["lon"],
            "appid": api_key,
            "units": "metric",
        }
    except Exception as e:
        return f"위치 정보를 받아올수없습니다. 오류 : {str(e)}"

    try:
        # API 요청 및 응답 처리
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"{location}의 현재 날씨: {weather_description}, 온도: {temperature}°C"
    except requests.exceptions.RequestException as e:
        return f"날씨 정보를 가져오는데 실패했습니다. 오류: {str(e)}"
