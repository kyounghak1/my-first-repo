
import requests
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Weather Dashboard", page_icon="☁️", layout="wide")

@st.cache_data(show_spinner=False, ttl=3600)
def geocode(city: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    r = requests.get(url, params={"name": city, "count": 1, "language": "en", "format": "json"}, timeout=10)
    r.raise_for_status()
    data = r.json()
    if not data.get("results"):
        return None
    res = data["results"][0]
    return {
        "name": res["name"],
        "lat": res["latitude"],
        "lon": res["longitude"],
        "country": res.get("country", ""),
        "timezone": res.get("timezone", "UTC"),
    }

@st.cache_data(show_spinner=False, ttl=900)
def fetch_forecast(lat: float, lon: float, timezone: str):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m","relative_humidity_2m","apparent_temperature","is_day","wind_speed_10m","weather_code"],
        "daily": ["temperature_2m_max","temperature_2m_min","precipitation_probability_max"],
        "hourly": ["temperature_2m"],
        "timezone": timezone,
        "forecast_days": 7,
        "past_days": 0,
    }
    r = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=10)
    r.raise_for_status()
    return r.json()

WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Dense drizzle",
    56: "Freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Rain showers",
    81: "Rain showers",
    82: "Violent rain showers",
    85: "Snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}

def show_current(card, place, forecast):
    current = forecast["current"]
    code = current.get("weather_code")
    label = WEATHER_CODE_MAP.get(code, "Unknown")
    with card:
        st.subheader(f"Now in {place['name']}, {place['country']}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature (°C)", f"{current['temperature_2m']:.1f}")
        col2.metric("Feels like (°C)", f"{current['apparent_temperature']:.1f}")
        col3.metric("Humidity (%)", f"{current['relative_humidity_2m']}")
        st.caption(f"Condition: {label} | Wind: {current['wind_speed_10m']} km/h | Timezone: {place['timezone']}")

def plot_daily_temperatures(forecast):
    d = forecast["daily"]
    dates = [datetime.fromisoformat(x).date() for x in d["time"]]
    tmax = d["temperature_2m_max"]
    tmin = d["temperature_2m_min"]

    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(dates, tmax, marker="o", label="Max °C")
    ax.plot(dates, tmin, marker="o", label="Min °C")
    ax.set_title("7-day Temperatures")
    ax.set_xlabel("Date")
    ax.set_ylabel("°C")
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig, clear_figure=True)

def plot_daily_rain_prob(forecast):
    d = forecast["daily"]
    dates = [datetime.fromisoformat(x).date() for x in d["time"]]
    pp = d["precipitation_probability_max"]

    fig, ax = plt.subplots(figsize=(7,4))
    ax.bar(dates, pp)
    ax.set_title("Daily Precipitation Probability")
    ax.set_xlabel("Date")
    ax.set_ylabel("%")
    ax.grid(True, axis="y", alpha=0.3)
    st.pyplot(fig, clear_figure=True)

# UI
st.title("☁️ Real-time Weather Dashboard")

with st.sidebar:
    st.header("Location")
    default_city = "Seoul"
    city = st.text_input("City name", value=default_city, placeholder="e.g., Seoul, Tokyo, New York")
    preset = st.selectbox("Quick select", ["Seoul","Tokyo","New York","London","Paris","Singapore","Sydney"])
    if st.button("Use quick select"):
        city = preset

if not city:
    st.info("Enter a city to begin.")
    st.stop()

place = geocode(city)
if place is None:
    st.error("City not found. Try a different name.")
    st.stop()

try:
    forecast = fetch_forecast(place["lat"], place["lon"], place["timezone"])
except Exception as e:
    st.error(f"Failed to fetch forecast: {e}")
    st.stop()

colA, colB = st.columns([1, 1])
show_current(colA, place, forecast)
with colB:
    st.subheader("7-day Overview")
    plot_daily_temperatures(forecast)
    plot_daily_rain_prob(forecast)

st.caption("Data: Open-Meteo.com | No API key required")
