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


def fetch_google_calendar_events(current_time: datetime, interval: int = 0) -> dict:
    """
    google calendar 에 등록된 스케쥴을 가져옵니다.
    """
    if interval < 0:
        start_time = (current_time + timedelta(days=interval)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_time = current_time.replace(
            hour=23, minute=59, second=59, microsecond=999999
        )
    elif interval == 0:
        start_time = current_time
        end_time = current_time.replace(
            hour=23, minute=59, second=59, microsecond=999999
        )
    else:
        start_time = (current_time + timedelta(days=interval)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_time = (current_time + timedelta(days=interval)).replace(
            hour=23, minute=59, second=59, microsecond=999999
        )

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
            "timeMin": start_time.isoformat().replace("+00:00", "Z"),
            "timeMax": end_time.isoformat().replace("+00:00", "Z"),
        },
    )
    return response.json()


# time_zone = pytz.timezone("Asia/Seoul")
# current_time = datetime.now(time_zone)
#
# print(fetch_google_calendar_events(current_time))
