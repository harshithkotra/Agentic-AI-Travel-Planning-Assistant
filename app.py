
import streamlit as st
import json
import os
import requests
from datetime import datetime

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Travel Planning Assistant",
    page_icon="✈️",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


# =====================================================
# DATA LOADING
# =====================================================

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_data(data):
    """Convert JSON data into a list of records."""
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        # Common dataset structures
        for key in ["data", "results", "items", "flights", "hotels", "places"]:
            if key in data and isinstance(data[key], list):
                return data[key]

        return list(data.values())

    return []


def get_value(item, *keys, default=None):
    """Get a value from a dictionary using flexible field names."""
    if not isinstance(item, dict):
        return default

    # Exact match
    for key in keys:
        if key in item and item[key] is not None:
            return item[key]

    # Case-insensitive match
    lower_keys = {str(k).lower(): v for k, v in item.items()}

    for key in keys:
        if key.lower() in lower_keys and lower_keys[key.lower()] is not None:
            return lower_keys[key.lower()]

    return default


def safe_number(value, default=0):
    try:
        return float(str(value).replace(",", "").replace("₹", "").strip())
    except (TypeError, ValueError):
        return default


def get_city(item, *keys):
    return str(get_value(item, *keys, default="")).strip()


# Load datasets safely
try:
    flights_data = normalize_data(load_json("flights.json"))
    hotels_data = normalize_data(load_json("hotels.json"))
    places_data = normalize_data(load_json("places.json"))
    DATA_LOADED = True

except Exception as e:
    flights_data = []
    hotels_data = []
    places_data = []
    DATA_LOADED = False
    DATA_ERROR = str(e)


# =====================================================
# CITY COORDINATES
# =====================================================

coordinates = {
    "goa": (15.2993, 74.1240),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946),
    "delhi": (28.6139, 77.2090),
    "hyderabad": (17.3850, 78.4867),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "jaipur": (26.9124, 75.7873),
    "pune": (18.5204, 73.8567)
}


# =====================================================
# WEATHER TOOL
# =====================================================

def get_weather(city):
    """Fetch live forecast from Open-Meteo."""
    city_key = city.lower().strip()

    if city_key not in coordinates:
        return None

    lat, lon = coordinates[city_key]

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": (
            "temperature_2m_max,temperature_2m_min,"
            "precipitation_probability_max"
        ),
        "timezone": "auto",
        "forecast_days": 3
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("daily")

    except Exception:
        return None


# =====================================================
# FLIGHT SEARCH
# =====================================================

def search_flights(source, destination):
    results = []

    for f in flights_data:

        flight_source = str(get_value(
            f,
            "source", "from", "origin", "departure_city",
            "from_city", "source_city", "departure",
            default=""
        ))

        flight_destination = str(get_value(
            f,
            "destination", "to", "arrival_city",
            "destination_city", "to_city", "dest",
            default=""
        ))

        price = safe_number(get_value(
            f,
            "price", "fare", "ticket_price", "cost",
            "flight_price", "amount", default=0
        ))

        if (
            flight_source.lower().strip() == source.lower().strip()
            and flight_destination.lower().strip() == destination.lower().strip()
        ):
            results.append({
                "airline": get_value(
                    f, "airline", "airline_name", "carrier", default="Airline"
                ),
                "source": flight_source,
                "destination": flight_destination,
                "price": price,
                "departure": get_value(
                    f, "departure_time", "departure", "depart", default="09:00"
                ),
                "arrival": get_value(
                    f, "arrival_time", "arrival", "arrive", default="11:00"
                ),
                "duration": get_value(
                    f, "duration", "travel_time", default="2 hours"
                )
            })

    results.sort(key=lambda x: x["price"])

    # Sample fallback for demonstration if route isn't in the dataset
    if not results:
        results = [{
            "airline": "Demo Air (Sample)",
            "source": source,
            "destination": destination,
            "price": 4500,
            "departure": "06:00",
            "arrival": "08:00",
            "duration": "2 hours",
            "sample": True
        }]

    return results


# =====================================================
# HOTEL SEARCH
# =====================================================

def search_hotels(city, travel_style):
    results = []

    for h in hotels_data:

        hotel_city = str(get_value(
            h, "city", "location", "destination", "hotel_city",
            default=""
        ))

        price = safe_number(get_value(
            h, "price_per_night", "price", "nightly_price",
            "cost_per_night", "rate", default=0
        ))

        rating = safe_number(get_value(
            h, "rating", "stars", "hotel_rating", "reviews_rating",
            default=3
        ))

        hotel_name = get_value(
            h, "name", "hotel_name", "property_name",
            default="Hotel"
        )

        hotel_type = get_value(
            h, "type", "category", "hotel_type",
            default="Hotel"
        )

        if hotel_city.lower().strip() == city.lower().strip():
            results.append({
                "name": hotel_name,
                "city": hotel_city,
                "price_per_night": price,
                "rating": rating,
                "type": hotel_type
            })

    if travel_style == "Budget":
        results.sort(key=lambda x: x["price_per_night"])

    elif travel_style == "Luxury":
        results.sort(key=lambda x: x["rating"], reverse=True)

    else:
        results.sort(key=lambda x: x["rating"], reverse=True)

    if not results:
        results = [{
            "name": f"{city} Comfort Stay (Sample)",
            "city": city,
            "price_per_night": 2500,
            "rating": 4.2,
            "type": "Sample Hotel"
        }]

    return results


# =====================================================
# PLACES DISCOVERY
# =====================================================

def search_places(city, interests):
    results = []

    for p in places_data:

        place_city = str(get_value(
            p, "city", "location", "destination",
            default=""
        ))

        category = str(get_value(
            p, "category", "type", "interest", "place_type",
            default="Other"
        ))

        rating = safe_number(get_value(
            p, "rating", "stars", "place_rating",
            default=4.0
        ))

        cost = safe_number(get_value(
            p, "estimated_cost", "cost", "entry_fee", "price",
            default=0
        ))

        name = get_value(
            p, "name", "place_name", "attraction", "title",
            default="Tourist Attraction"
        )

        if place_city.lower().strip() == city.lower().strip():

            if not interests or category.lower() in [
                interest.lower() for interest in interests
            ]:
                results.append({
                    "name": name,
                    "city": place_city,
                    "category": category,
                    "rating": rating,
                    "estimated_cost": cost
                })

    if not results:
        for p in places_data:

            place_city = str(get_value(
                p, "city", "location", "destination", default=""
            ))

            if place_city.lower().strip() == city.lower().strip():
                results.append({
                    "name": get_value(
                        p, "name", "place_name", "title",
                        default="Attraction"
                    ),
                    "city": city,
                    "category": get_value(
                        p, "category", "type", default="Other"
                    ),
                    "rating": safe_number(
                        get_value(p, "rating", "stars", default=4)
                    ),
                    "estimated_cost": safe_number(
                        get_value(p, "estimated_cost", "cost", "price", default=0)
                    )
                })

    results.sort(key=lambda x: x["rating"], reverse=True)

    # Sample places if dataset doesn't contain destination records
    if not results:
        results = [
            {
                "name": f"{city} City Sightseeing",
                "city": city,
                "category": "Sightseeing",
                "rating": 4.5,
                "estimated_cost": 500
            },
            {
                "name": f"{city} Local Market",
                "city": city,
                "category": "Shopping",
                "rating": 4.2,
                "estimated_cost": 500
            },
            {
                "name": f"{city} Nature Spot",
                "city": city,
                "category": "Nature",
                "rating": 4.6,
                "estimated_cost": 500
            }
        ]

    return results


# =====================================================
# BUDGET ESTIMATION
# =====================================================

def calculate_budget(flight_price, hotel_price, nights, places, days):
    flight_cost = flight_price
    accommodation_cost = hotel_price * nights
    food_cost = 1000 * days
    attraction_cost = sum(p["estimated_cost"] for p in places[:days * 2])

    total = flight_cost + accommodation_cost + food_cost + attraction_cost

    return {
        "flight": flight_cost,
        "hotel": accommodation_cost,
        "food": food_cost,
        "attractions": attraction_cost,
        "total": total
    }


# =====================================================
# WEATHER DESCRIPTION
# =====================================================

def weather_description(code):
    mapping = {
        0: "Clear Sky ☀️",
        1: "Mainly Clear 🌤️",
        2: "Partly Cloudy ⛅",
        3: "Cloudy ☁️",
        45: "Fog 🌫️",
        48: "Fog 🌫️",
        51: "Light Drizzle 🌦️",
        61: "Light Rain 🌧️",
        63: "Moderate Rain 🌧️",
        65: "Heavy Rain 🌧️",
        71: "Snow ❄️",
        80: "Rain Showers 🌦️",
        95: "Thunderstorm ⛈️"
    }

    return mapping.get(code, "Weather conditions vary 🌤️")


# =====================================================
# USER INTERFACE
# =====================================================

st.sidebar.header("🌍 Plan Your Trip")

source = st.sidebar.text_input("Starting City", "Hyderabad")

destination = st.sidebar.selectbox(
    "Destination",
    ["Goa", "Mumbai", "Bangalore", "Delhi", "Chennai", "Kolkata", "Jaipur", "Pune"]
)

days = st.sidebar.slider("Trip Duration (Days)", 1, 7, 3)

budget = st.sidebar.number_input(
    "Total Budget (₹)",
    min_value=1000,
    max_value=200000,
    value=15000,
    step=1000
)

travel_style = st.sidebar.selectbox(
    "Travel Style",
    ["Budget", "Standard", "Luxury"]
)

interests = st.sidebar.multiselect(
    "Your Interests",
    ["Beach", "Historical", "Nature", "Shopping"],
    default=["Beach", "Historical"]
)

generate = st.sidebar.button("✨ Generate My Trip", use_container_width=True)

# =====================================================
# MAIN SCREEN
# =====================================================

st.title("✈️ AI Travel Planning Assistant")

st.markdown(
    "Your smart travel companion for flights, hotels, weather and itineraries."
)

st.info(
    "Select your travel preferences and generate a personalized trip plan."
)

if not DATA_LOADED:
    st.error(f"Dataset loading issue: {DATA_ERROR}")

# =====================================================
# GENERATE TRIP
# =====================================================

if generate:

    if not source.strip():
        st.error("Please enter your starting city.")
        st.stop()

    with st.spinner("Preparing your personalized trip..."):

        flight_options = search_flights(source, destination)
        hotel_options = search_hotels(destination, travel_style)
        places = search_places(destination, interests)

        flight = flight_options[0]
        hotel = hotel_options[0]

        nights = max(days - 1, 1)

        budget_data = calculate_budget(
            flight["price"],
            hotel["price_per_night"],
            nights,
            places,
            days
        )

        weather = get_weather(destination)

    # =================================================
    # SUMMARY
    # =================================================

    st.success("Your travel itinerary is ready!")

    st.header(f"🧳 Your {days}-Day Trip to {destination}")

    c1, c2, c3 = st.columns(3)

    c1.metric("✈️ Flight Cost", f"₹{flight['price']:,.0f}")
    c2.metric("🏨 Accommodation", f"₹{budget_data['hotel']:,.0f}")
    c3.metric("💰 Total Estimate", f"₹{budget_data['total']:,.0f}")

    # =================================================
    # FLIGHT
    # =================================================

    st.subheader("✈️ Flight Recommendation")

    st.write(f"**Airline:** {flight['airline']}")
    st.write(f"**Route:** {flight['source']} → {flight['destination']}")
    st.write(f"**Departure:** {flight['departure']}")
    st.write(f"**Arrival:** {flight['arrival']}")
    st.write(f"**Duration:** {flight['duration']}")
    st.write(f"**Price:** ₹{flight['price']:,.0f}")

    if flight.get("sample"):
        st.caption("Sample flight data used because no matching route was available.")

    # =================================================
    # HOTEL
    # =================================================

    st.subheader("🏨 Hotel Recommendation")

    st.write(f"**Hotel:** {hotel['name']}")
    st.write(f"**Hotel Type:** {hotel['type']}")
    st.write(f"**Rating:** ⭐ {hotel['rating']}/5")
    st.write(f"**Price per night:** ₹{hotel['price_per_night']:,.0f}")
    st.write(f"**Number of Nights:** {nights}")

    # =================================================
    # WEATHER
    # =================================================

    st.subheader("🌦️ Live Weather Forecast")

    if weather:

        weather_days = weather.get("time", [])

        for i in range(min(days, len(weather_days))):

            date = weather_days[i]
            maximum = weather.get("temperature_2m_max", [])[i]
            minimum = weather.get("temperature_2m_min", [])[i]
            rain = weather.get("precipitation_probability_max", [0] * len(weather_days))[i]

            st.write(
                f"**{date}** | "
                f"🌡️ {minimum}°C – {maximum}°C | "
                f"🌧️ Rain probability: {rain}%"
            )

    else:
        st.warning("Live weather unavailable at this moment.")

    # =================================================
    # ITINERARY
    # =================================================

    st.subheader("🗓️ Day-wise Travel Itinerary")

    if places:

        for day in range(days):

            st.markdown(f"### Day {day + 1}")

            day_places = places[day * 2: day * 2 + 2]

            if day_places:

                for place in day_places:

                    st.markdown(
                        f"📍 **{place['name']}**  \n"
                        f"Category: {place['category']} | "
                        f"⭐ {place['rating']} | "
                        f"Estimated cost: ₹{place['estimated_cost']:,.0f}"
                    )

            else:
                st.write("Enjoy local food, shopping and city exploration.")

    # =================================================
    # BUDGET
    # =================================================

    st.subheader("💰 Budget Breakdown")

    st.write(f"✈️ Flight: ₹{budget_data['flight']:,.0f}")
    st.write(f"🏨 Hotel: ₹{budget_data['hotel']:,.0f}")
    st.write(f"🍽️ Food: ₹{budget_data['food']:,.0f}")
    st.write(f"📍 Attractions: ₹{budget_data['attractions']:,.0f}")

    st.markdown(f"## Total Estimated Cost: ₹{budget_data['total']:,.0f}")

    if budget_data["total"] <= budget:
        st.success(f"Your trip is within your budget of ₹{budget:,.0f}!")
    else:
        st.warning(f"Estimated trip cost exceeds your budget of ₹{budget:,.0f}.")

    # =================================================
    # REASONING
    # =================================================

    st.subheader("🤖 Why These Recommendations?")

    st.write(
        f"- Flight: Selected the lowest-priced available matching flight "
        f"or sample flight for {source} to {destination}."
    )

    st.write(
        f"- Hotel: Selected based on your {travel_style.lower()} travel preference."
    )

    st.write(
        "- Attractions: Selected according to your interests and available ratings."
    )

    st.write(
        "- Weather: Retrieved from Open-Meteo when available."
    )

    # =================================================
    # DISCLAIMER
    # =================================================

    st.caption(
        "Academic demonstration project. Flights, hotels and attraction prices "
        "are sample dataset estimates and are not live booking prices."
    )

# =====================================================
# FEATURES
# =====================================================

st.markdown("---")

st.subheader("🌟 Project Features")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Flight Search", "JSON Dataset")
col2.metric("Hotel Finder", "JSON Dataset")
col3.metric("Weather", "Live API")
col4.metric("Trip Planner", "Automated")

st.markdown("---")

st.caption(
    "Agentic AI Travel Planning Assistant | Python | LangChain | Streamlit | Open-Meteo"
)
