from pydantic import BaseModel
from typing import List, Optional


class NormalizedWeather(BaseModel):
    temperature: float
    condition: str
    extreme: bool


class NormalizedAQI(BaseModel):
    aqi: int
    category: str


class NewsEvent(BaseModel):
    title: str
    source: str
    url: str
    published_at: str
    keyword_triggered: str


class NormalizedNews(BaseModel):
    negative_event_count: int
    events: List[NewsEvent]
