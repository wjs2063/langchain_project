from aiohttp import ClientSession
import jwt
import time
import os
from dotenv import load_dotenv
from aiohttp import ClientSession

load_dotenv()


class GoogleCalendarHandler:

    @staticmethod
    async def fetch_calendar_events(calendar_id: str):
        async with ClientSession() as session:
            async with session.get(
                f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events?key=<KEY>"
            ) as response:
                return await response.json()

    @staticmethod
    async def register_calendar_event(calendar_id: str, event: dict):
        async with ClientSession() as session:
            async with session.post(
                f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events?key=<KEY>",
                json=event,
            ) as response:
                pass

    @staticmethod
    async def delete_calendar_event(calendar_id: str, event_id: str):
        pass

    @staticmethod
    async def fetch_google_calendar_access_token(signed_jwt: str = None):
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
        async with ClientSession() as session:
            async with session.post(url=google_oauth_url, json=data) as response:
                response = await response.json()
                return response["access_token"]


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
