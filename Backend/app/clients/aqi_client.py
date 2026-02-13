import httpx
from app.config import settings
from app.models.internal_models import NormalizedAQI


class AQIClient:

    BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

    async def get_aqi(self, lat: float, lon: float):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": settings.WEATHER_API_KEY
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        aqi = data["list"][0]["main"]["aqi"]

        category_map = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }

        return NormalizedAQI(
            aqi=aqi,
            category=category_map.get(aqi, "Unknown")
        )
