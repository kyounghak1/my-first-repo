# multi-arch 지원(ARM/Intel 맥 둘 다 OK)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHERUSAGESTATS=false \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8501

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# 소스 복사
COPY Weather_Dashboard/ ./Weather_Dashboard/

EXPOSE 8501
CMD ["python", "-m", "streamlit", "run", "Weather_Dashboard/weather_dashboard.py"]