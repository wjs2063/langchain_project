import jwt
import time
import os
import json
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import pytz

load_dotenv()


def create_google_jwt_token():
    iat = time.time()
    exp = iat + 3600
    payload = {
        "iss": os.getenv("MY_GOOGLE_CALENDAR_EMAIL"),
        # "sub": os.getenv("MY_GOOGLE_CALENDAR_ID"),
        "scope": "https://www.googleapis.com/auth/calendar.readonly",
        "aud": "https://oauth2.googleapis.com/token",
        "iat": iat,
        "exp": exp,
    }
    additional_headers = {"kid": os.getenv("GOOGLE_CALENDAR_SERVICE_KEY_ID")}
    signed_jwt = jwt.encode(
        payload,
        os.getenv("GOOGLE_CALENDAR_SERVICE_KEY_PASSWORD"),
        headers=additional_headers,
        algorithm="RS256",
    )
    return signed_jwt


def fetch_google_calendar_access_token():
    signed_jwt = create_google_jwt_token()

    google_oauth_url = "https://oauth2.googleapis.com/token"
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": signed_jwt,
    }
    response = requests.post(google_oauth_url, data=data)
    return response.json()["access_token"]


# 200 OK 코드가 아닌 경우 exception 발생
# response.raise_for_status()


def get_google_calendar_events(time_min: datetime, interval: int = 1) -> dict:
    """
    google calendar 에 등록된 스케쥴을 가져옵니다.
    """
    time_min, time_max = min([time_min, time_min + timedelta(days=interval)]), max(
        [time_min, time_min + timedelta(days=interval)]
    )
    # time_max = (time_min + timedelta(days=interval)).isoformat().replace("+00:00", "Z")
    print(time_min, time_max)
    access_token = fetch_google_calendar_access_token()
    calendar_id = os.getenv("MY_GOOGLE_CALENDAR_USER_ID")
    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(
        url,
        headers=header,
        params={
            "timeMin": time_min.isoformat().replace("+00:00", "Z"),
            "timeMax": time_max.isoformat().replace("+00:00", "Z"),
        },
    )
    return response.json()


# time_zone = pytz.timezone("Asia/Seoul")
# current_time = datetime.now(time_zone)
#
# print(fetch_google_calendar_events(current_time))
