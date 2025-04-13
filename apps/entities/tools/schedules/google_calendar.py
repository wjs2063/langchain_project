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
    """
    Generate a Google JWT token for authentication

    This function creates a JSON Web Token (JWT) to authenticate with Google API services.
    The payload includes information such as the issuing entity, scope, audience, issued time,
    and expiration time. The token is signed using RS256 algorithm.

    Returns:
        str: The signed JWT token.

    Raises:
        EnvironmentError: If one or more of the required environment variables are not set.
    """
    iat = time.time()
    exp = iat + 3600
    payload = {
        "iss": os.getenv("MY_GOOGLE_CALENDAR_EMAIL"),
        # "sub": os.getenv("MY_GOOGLE_CALENDAR_ID"),
        "scope": "https://www.googleapis.com/auth/calendar",
        # "https://www.googleapis.com/auth/calendar.readonly",
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
    """
    Fetches an access token for Google Calendar API using a signed JWT.

    This function creates a signed JWT token and exchanges it for an access token
    from Google's OAuth 2.0 endpoint. The access token is required for making
    authenticated requests to the Google Calendar API.

    Returns:
        str: The obtained access token for accessing Google Calendar API.

    Raises:
        KeyError: If the response JSON does not contain the "access_token" key.
    """
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
    Fetch events from a Google Calendar within a specific time interval.

    This function retrieves a list of events available on a Google Calendar
    for a given time period defined by the provided `current_time` and optional
    `interval`. It constructs a request to the Google Calendar API to fetch events
    that fall between the computed time boundaries.

    Parameters:
        current_time (datetime): The reference datetime used to calculate the
                                 range of events to fetch.
        interval (int, optional): The number of days to adjust the time range
                                  relative to `current_time`. Defaults to 0. A
                                  positive value fetches events for a future
                                  day, and a negative value fetches events for
                                  a past day.

    Returns:
        dict: The JSON response from the Google Calendar API containing calendar
              events. The structure includes event details such as title, time,
              and location, depending on the calendar configuration.
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


def insert_google_calendar_events(
    summary: str, description: str, requested_start_time: datetime, interval: int = 30
) -> dict:
    """
    Inserts an event into the user's Google Calendar with the provided details.

    This function facilitates the creation of a Google Calendar event. It converts
    the provided start time into the required format, calculates the end time
    based on a specified interval, and makes a POST request to the Google Calendar
    API. The event is created in the user's calendar, and the API's response is
    returned. The function requires that the access token and calendar ID are
    provided through environment variables or fetched directly.

    Args:
        summary (str): Title of the event to be added.
        description (str): Detailed description of the event.
        requested_start_time (datetime): The start time of the event in datetime format.
        interval (int): Duration of the event in minutes. Defaults to 30 minutes.

    Returns:
        dict: Response from the Google Calendar API containing event details, status,
        or errors if any occur.
    """
    access_token = fetch_google_calendar_access_token()
    calendar_id = os.getenv("MY_GOOGLE_CALENDAR_USER_ID")
    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    start_time = requested_start_time
    end_time = start_time + timedelta(minutes=interval)
    response = requests.post(
        url,
        headers=header,
        json={
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Seoul"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Seoul"},
        },
    )
    return response.json()


time_zone = pytz.timezone("Asia/Seoul")
current_time = datetime.now(time_zone)
# print(insert_google_calendar_events(current_time))
