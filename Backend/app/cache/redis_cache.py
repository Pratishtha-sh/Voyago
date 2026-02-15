import redis
import json
from app.config import settings


class RedisCache:

    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )

    def get(self, key: str):
        data = self.client.get(key)
        if data:
            return json.loads(data)
        return None

    def set(self, key: str, value: dict, ttl: int = 21600):
        # Default TTL = 6 hours
        self.client.setex(key, ttl, json.dumps(value))


cache = RedisCache()
