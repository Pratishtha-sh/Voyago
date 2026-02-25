from fastapi import APIRouter, Request, HTTPException
from app.models.request_models import TravelAnalyzeRequest
from app.services.travel_service import TravelService
from app.db.repository import TripRepository
from app.middleware.rate_limit import limiter

router = APIRouter(prefix="/travel", tags=["Travel"])

travel_service = TravelService()
repository = TripRepository()


@router.post("/analyze")
@limiter.limit("10/minute")
async def analyze_travel(request: Request, payload: TravelAnalyzeRequest):
    try:
        result = await travel_service.analyze_travel(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trip/{report_id}")
@limiter.limit("10/minute")
async def get_trip(request: Request, report_id: str):
    trip = await repository.get_trip(report_id)

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    trip["_id"] = str(trip["_id"])
    return trip


@router.delete("/trip/{report_id}")
@limiter.limit("10/minute")
async def delete_trip(request: Request, report_id: str):
    result = await repository.delete_trip(report_id)

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Trip not found")

    return {"message": "Trip deleted successfully"}
