from app.config import settings
from app.clients.base_client import BaseClient
from app.models.internal_models import NormalizedAQI


class AQIClient(BaseClient):

    BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

    async def get_aqi(self, lat: float, lon: float):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": settings.WEATHER_API_KEY
        }

        response = await self.client.get(self.BASE_URL, params=params)
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
