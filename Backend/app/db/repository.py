from app.db.mongo import mongodb
from datetime import datetime


class TripRepository:
    """
    Trip Storage — saves and retrieves user trip plans.
    No longer stores risk reports; stores contextual travel analyses
    that can be retrieved, extended as saved itineraries.
    """

    def __init__(self):
        self.collection = mongodb.get_collection("trips")

    async def save_trip(self, trip_data: dict):
        trip_data["saved_at"] = datetime.utcnow()
        await self.collection.insert_one(trip_data)

    async def get_trip(self, report_id: str):
        return await self.collection.find_one({"report_id": report_id})

    async def delete_trip(self, report_id: str):
        return await self.collection.delete_one({"report_id": report_id})
