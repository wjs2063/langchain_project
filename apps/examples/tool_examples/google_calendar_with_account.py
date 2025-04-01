import jwt
import time
import os
import json
from dotenv import load_dotenv
import requests

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

    URL = "https://oauth2.googleapis.com/token"
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": signed_jwt,
    }
    response = requests.post(URL, data=data)
    return response.json()["access_token"]


# 200 OK 코드가 아닌 경우 exception 발생
# response.raise_for_status()


def get_google_calendar_events():
    access_token = fetch_google_calendar_access_token()
    calendar_id = os.getenv("MY_GOOGLE_CALENDAR_USER_ID")
    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(url, headers=header)
    # print(response.json())
    return response.json()


# get_google_calendar_events()
