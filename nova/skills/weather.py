import requests
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
import os

load_dotenv()

def format_date(date_string):
    forecast_date = datetime.strptime(
        date_string, "%Y-%m-%d"
    ).date()

    today = date.today()

    if forecast_date == today:
        return "Today"

    if forecast_date == today + timedelta(days=1):
        return "Tomorrow"

    return forecast_date.strftime("%A")

URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": os.getenv("LAT"),
    "longitude": os.getenv("LONG"),
    "daily": "weather_code,rain_sum",
    "timezone": "Pacific/Auckland",
}

WMO_CODES = {
    0: "Clear",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Freezing fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Freezing drizzle",
    57: "Heavy freezing drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Light rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    85: "Light snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with light hail",
    99: "Thunderstorm with heavy hail",
}


def weather():
    response = requests.get(URL, params=PARAMS, timeout=10)
    response.raise_for_status()

    daily = response.json()["daily"]

    return [
        {
            "date": format_date(date),
            "condition": WMO_CODES.get(code, "Unknown"),
            "rainfall": (
                f"{round(rain, 1)} millimeters"
                if rain > 0
                else "no rainfall"
            )
        }
        for date, code, rain in zip(
            daily["time"],
            daily["weather_code"],
            daily["rain_sum"],
        )
    ]
