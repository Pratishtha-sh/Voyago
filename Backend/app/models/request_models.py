from pydantic import BaseModel, Field
from datetime import date


class TravelAnalyzeRequest(BaseModel):
    source_city: str = Field(..., min_length=2)
    destination_city: str = Field(..., min_length=2)
    travel_date: date
    duration_days: int = Field(..., gt=0)
