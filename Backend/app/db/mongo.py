from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


class MongoDB:

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.client.get_default_database()

    def get_collection(self, name: str):
        return self.db[name]


mongodb = MongoDB()
