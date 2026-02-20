from fastapi import APIRouter, Request, HTTPException
from app.models.request_models import TravelAnalyzeRequest
from app.services.travel_service import TravelService
from app.db.repository import TravelRepository
from app.middleware.rate_limit import limiter

router = APIRouter(prefix="/travel", tags=["Travel"])

travel_service = TravelService()
repository = TravelRepository()


@router.post("/analyze")
@limiter.limit("10/minute")
async def analyze_travel(request: Request, payload: TravelAnalyzeRequest):
    try:
        result = await travel_service.analyze_travel(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report/{report_id}")
@limiter.limit("10/minute")
async def get_report(request: Request, report_id: str):
    report = await repository.get_report(report_id)

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report["_id"] = str(report["_id"])
    return report


@router.delete("/report/{report_id}")
@limiter.limit("10/minute")
async def delete_report(request: Request, report_id: str):
    result = await repository.delete_report(report_id)

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Report not found")

    return {"message": "Report deleted successfully"}
