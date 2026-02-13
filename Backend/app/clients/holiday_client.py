from app.config import settings
from app.clients.base_client import BaseClient
from app.models.internal_models import NormalizedHoliday


class HolidayClient(BaseClient):

    BASE_URL = "https://calendarific.com/api/v2/holidays"

    async def get_holiday(self, country: str, year: int):
        params = {
            "api_key": settings.HOLIDAY_API_KEY,
            "country": country,
            "year": year
        }

        response = await self.client.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        holidays = data.get("response", {}).get("holidays", [])

        if holidays:
            return NormalizedHoliday(
                is_holiday=True,
                holiday_name=holidays[0]["name"]
            )

        return NormalizedHoliday(
            is_holiday=False,
            holiday_name=None
        )
