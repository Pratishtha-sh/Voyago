import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    AQI_API_KEY = os.getenv("AQI_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    HOLIDAY_API_KEY = os.getenv("HOLIDAY_API_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    API_SECRET_KEY = os.getenv("API_SECRET_KEY")


settings = Settings()

RISK_WEIGHTS = {
    "weather": 0.30,
    "aqi": 0.35,
    "holiday": 0.15,
    "news": 0.20
}