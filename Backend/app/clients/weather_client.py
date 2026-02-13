from app.config import settings
from app.clients.base_client import BaseClient
from app.models.internal_models import NormalizedWeather


class WeatherClient(BaseClient):

    BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

    async def get_weather(self, lat: float, lon: float):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric"
        }

        response = await self.client.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        forecast = data["list"][0]

        temp = forecast["main"]["temp"]
        condition = forecast["weather"][0]["main"]

        extreme = temp > 40 or temp < 5 or condition in ["Storm", "Extreme"]

        return NormalizedWeather(
            temperature=temp,
            condition=condition,
            extreme=extreme
        )
