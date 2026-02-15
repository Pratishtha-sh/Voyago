import asyncio
import uuid
from datetime import datetime
from app.db.repository import TravelRepository
from app.clients.geo_client import GeoClient
from app.clients.weather_client import WeatherClient
from app.clients.aqi_client import AQIClient
from app.clients.holiday_client import HolidayClient
from app.clients.news_client import NewsClient
from app.services.scoring_engine import ScoringEngine


class TravelService:

    def __init__(self):
        self.geo_client = GeoClient()
        self.weather_client = WeatherClient()
        self.aqi_client = AQIClient()
        self.holiday_client = HolidayClient()
        self.news_client = NewsClient()
        self.scoring_engine = ScoringEngine()
        self.repository = TravelRepository()

    async def analyze_travel(self, request):

        # 1️⃣ Get destination coordinates
        geo_data = await self.geo_client.get_coordinates(request.destination_city)

        lat = geo_data["lat"]
        lon = geo_data["lon"]
        country = geo_data["country"]

        # 2️⃣ Run external API calls concurrently
        weather_task = self.weather_client.get_weather(lat, lon)
        aqi_task = self.aqi_client.get_aqi(lat, lon)
        holiday_task = self.holiday_client.get_holiday(country, request.travel_date.year)
        news_task = self.news_client.get_news_risk(request.destination_city)

        weather, aqi, holiday, news = await asyncio.gather(
            weather_task,
            aqi_task,
            holiday_task,
            news_task
        )

        # 3️⃣ Calculate risk
        risk_result = self.scoring_engine.calculate_total_score(
            weather,
            aqi,
            holiday,
            news,
            request.travel_date
        )

        # 4️⃣ Assemble response
        report_id = str(uuid.uuid4())

        response = {
            "report_id": report_id,
            "destination": {
                "city": request.destination_city,
                "country": country,
                "coordinates": {
                    "lat": lat,
                    "lon": lon
                }
            },
            "travel_date": str(request.travel_date),
            "duration_days": request.duration_days,
            "risk_analysis": {
                "risk_score": risk_result["risk_score"],
                "risk_level": risk_result["risk_level"],
                "factors": risk_result["factor_breakdown"]
            },
            "meta": {
                "cached": False,
                "generated_at": datetime.utcnow()
            },
            "explanations": risk_result["explanations"]
        }

        # 5️⃣ Save to MongoDB
        await self.repository.save_report(response)
    
        return response
