from app.config import settings
from app.clients.base_client import BaseClient


class GeoClient(BaseClient):

    BASE_URL = "https://api.openweathermap.org/geo/1.0/direct"

    async def get_coordinates(self, city: str):
        params = {
            "q": city,
            "limit": 1,
            "appid": settings.WEATHER_API_KEY
        }

        response = await self.client.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            raise ValueError("City not found")

        return {
            "lat": data[0]["lat"],
            "lon": data[0]["lon"],
            "country": data[0]["country"]
        }
