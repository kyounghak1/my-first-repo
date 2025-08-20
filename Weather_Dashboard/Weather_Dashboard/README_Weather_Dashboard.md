
# Weather Dashboard (Streamlit + Open-Meteo)

Visual, interactive weather dashboard.

## Features
- City search with geocoding
- Current conditions: temperature, feels-like, humidity, wind, condition label
- 7-day charts: max/min temperature, precipitation probability
- Caching for fast reloads

## Run
1) Install dependencies:
   ```bash
   pip install streamlit requests matplotlib
   ```
2) Start the app:
   ```bash
   streamlit run weather_dashboard.py
   ```
3) Open the URL shown in the terminal.

## Notes
- Uses Open-Meteo. No API key.
- Default city is Seoul. Use the sidebar to change.
