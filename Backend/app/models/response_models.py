from pydantic import BaseModel
from typing import Dict
from datetime import datetime


class Coordinates(BaseModel):
    lat: float
    lon: float


class DestinationInfo(BaseModel):
    city: str
    country: str
    coordinates: Coordinates


class RiskFactors(BaseModel):
    weather_risk: int
    aqi_risk: int
    holiday_risk: int
    news_risk: int


class RiskAnalysis(BaseModel):
    risk_score: int
    risk_level: str
    factors: RiskFactors


class MetaInfo(BaseModel):
    cached: bool
    generated_at: datetime


class TravelAnalyzeResponse(BaseModel):
    report_id: str
    destination: DestinationInfo
    travel_date: str
    duration_days: int
    risk_analysis: RiskAnalysis
    meta: MetaInfo
