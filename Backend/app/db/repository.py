from app.db.mongo import mongodb
from datetime import datetime


class TravelRepository:

    def __init__(self):
        self.collection = mongodb.get_collection("reports")

    async def save_report(self, report_data: dict):
        report_data["created_at"] = datetime.utcnow()
        await self.collection.insert_one(report_data)

    async def get_report(self, report_id: str):
        return await self.collection.find_one({"report_id": report_id})

    async def delete_report(self, report_id: str):
        return await self.collection.delete_one({"report_id": report_id})
