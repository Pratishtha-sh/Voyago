import asyncio
import uuid
from datetime import datetime
from app.db.repository import TripRepository
from app.clients.geo_client import GeoClient
from app.clients.weather_client import WeatherClient
from app.clients.aqi_client import AQIClient
from app.clients.news_client import NewsClient
from app.services.insight_service import InsightService


class TravelService:

    def __init__(self):
        self.geo_client = GeoClient()
        self.weather_client = WeatherClient()
        self.aqi_client = AQIClient()
        self.news_client = NewsClient()
        self.repository = TripRepository()
        self.insight_service = InsightService()

    async def analyze_travel(self, request):

        # 1️⃣ Resolve destination coordinates
        geo_data = await self.geo_client.get_coordinates(request.destination_city)
        lat = geo_data["lat"]
        lon = geo_data["lon"]
        country = geo_data["country"]

        # 2️⃣ Fetch environmental & news data concurrently
        weather, aqi, news = await asyncio.gather(
            self.weather_client.get_weather(lat, lon),
            self.aqi_client.get_aqi(lat, lon),
            self.news_client.get_news_risk(request.destination_city)
        )

        # 3️⃣ Build contextual response payload
        response = {
            "report_id": str(uuid.uuid4()),
            "destination": {
                "city": request.destination_city,
                "country": country,
                "coordinates": {"lat": lat, "lon": lon}
            },
            "travel_date": str(request.travel_date),
            "duration_days": request.duration_days,
            "environment": {
                "weather": {
                    "temperature_celsius": weather.temperature,
                    "condition": weather.condition,
                    "extreme_conditions": weather.extreme
                },
                "air_quality": {
                    "aqi_index": aqi.aqi,
                    "category": aqi.category
                }
            },
            "news_context": {
                "negative_event_count": news.negative_event_count,
                "events": [
                    {
                        "title": e.title,
                        "source": e.source,
                        "keyword_triggered": e.keyword_triggered,
                        "published_at": e.published_at
                    }
                    for e in news.events
                ]
            },
            "meta": {
                "generated_at": datetime.utcnow().isoformat()
            }
        }

        # 4️⃣ Get LLM analysis of the contextual data
        ai_insight = await self.insight_service.generate_ai_insight(response)
        response["ai_insight"] = ai_insight

        return response
