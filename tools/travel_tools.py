
import json
import os
import requests
from langchain_core.tools import tool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


@tool
def search_flights(source: str, destination: str):
    """Search available flights between source and destination and return the cheapest options."""
    flights = load_data("flights.json")

    results = [
        flight for flight in flights
        if flight["source"].lower() == source.lower()
        and flight["destination"].lower() == destination.lower()
    ]

    return sorted(results, key=lambda x: x["price"])[:5]


@tool
def recommend_hotels(city: str, max_price: int = 10000):
    """Find hotels in a city within the maximum price per night, sorted by rating."""
    hotels = load_data("hotels.json")

    results = [
        hotel for hotel in hotels
        if hotel["city"].lower() == city.lower()
        and hotel["price_per_night"] <= max_price
    ]

    return sorted(results, key=lambda x: x["rating"], reverse=True)[:5]


@tool
def discover_places(city: str, category: str = "All"):
    """Find tourist attractions in a city, optionally filtering by category."""
    places = load_data("places.json")

    results = [
        place for place in places
        if place["city"].lower() == city.lower()
        and (
            category.lower() == "all"
            or place["category"].lower() == category.lower()
        )
    ]

    return sorted(results, key=lambda x: x["rating"], reverse=True)


@tool
def get_weather(city: str):
    """Get current forecast information from Open-Meteo for a supported city."""
    coordinates = {
        "goa": (15.2993, 74.1240),
        "hyderabad": (17.3850, 78.4867),
        "mumbai": (19.0760, 72.8777),
        "bangalore": (12.9716, 77.5946),
        "delhi": (28.6139, 77.2090)
    }

    if city.lower() not in coordinates:
        return "Weather location not supported."

    lat, lon = coordinates[city.lower()]

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": 3
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        return {
            "city": city,
            "daily_forecast": data.get("daily", {})
        }

    except requests.RequestException as error:
        return f"Weather API error: {str(error)}"


@tool
def estimate_budget(
    flight_cost: int,
    hotel_cost_per_night: int,
    nights: int,
    daily_expenses: int
):
    """Estimate total trip budget including flights, accommodation and daily expenses."""
    flight_total = flight_cost
    hotel_total = hotel_cost_per_night * nights
    local_total = daily_expenses * (nights + 1)

    return {
        "flight": flight_total,
        "hotel": hotel_total,
        "food_and_local_transport": local_total,
        "total_budget": flight_total + hotel_total + local_total
    }


ALL_TRAVEL_TOOLS = [
    search_flights,
    recommend_hotels,
    discover_places,
    get_weather,
    estimate_budget
]
