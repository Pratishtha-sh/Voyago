from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class Coordinates(BaseModel):
    lat: float
    lon: float


class DestinationInfo(BaseModel):
    city: str
    country: str
    coordinates: Coordinates


class WeatherInfo(BaseModel):
    temperature_celsius: float
    condition: str
    extreme_conditions: bool


class AirQualityInfo(BaseModel):
    aqi_index: int
    category: str


class EnvironmentInfo(BaseModel):
    weather: WeatherInfo
    air_quality: AirQualityInfo


class NewsEventInfo(BaseModel):
    title: str
    source: str
    keyword_triggered: str
    published_at: str


class NewsContext(BaseModel):
    negative_event_count: int
    events: List[NewsEventInfo]


class AIInsight(BaseModel):
    weather_explanation: str
    air_quality_explanation: str
    news_explanation: str
    advisory: str
    precautions: List[str]
    tips: List[str]


class MetaInfo(BaseModel):
    generated_at: str


class TravelAnalyzeResponse(BaseModel):
    report_id: str
    destination: DestinationInfo
    travel_date: str
    duration_days: int
    environment: EnvironmentInfo
    news_context: NewsContext
    ai_insight: Optional[AIInsight]
    meta: MetaInfo
