from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim
from langchain_core.tools import Tool, tool

# locator = Nominatim(user_agent="geo_info", adapter_factory=AioHTTPAdapter)
locator = Nominatim(user_agent="geo_info")


@tool
def fetch_coordination_tool(location) -> dict[str, str]:
    """
    Fetches the geographical coordinates for a given location string.

    This function utilizes the `locator.geocode` method to find the
    latitude and longitude of a location and returns a dictionary
    containing the coordinates.

    Args:
        location (str): The name or address of the location to fetch
            coordinates for.

    Returns:
        dict[str, str]: A dictionary containing the latitude and longitude
            as string values with keys 'lat' and 'lon'.

    Raises:
        TypeError: If `location` is not a string.
        ValueError: If the geocoding process fails or if `response` does
            not contain expected keys.
    """
    response = locator.geocode(location)
    return {"lat": response["latitude"], "lon": response["longitude"]}


# print(locator.geocode("서울 천호동").raw)
