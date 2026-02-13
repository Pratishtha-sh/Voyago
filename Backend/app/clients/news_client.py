from datetime import datetime, timedelta
from app.config import settings
from app.clients.base_client import BaseClient
from app.models.internal_models import NormalizedNews


class NewsClient(BaseClient):

    BASE_URL = "https://newsapi.org/v2/everything"

    NEGATIVE_KEYWORDS = [
        "protest",
        "riot",
        "strike",
        "flood",
        "storm",
        "conflict",
        "violence",
        "disaster"
    ]

    async def get_news_risk(self, city: str):
        from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

        params = {
            "q": city,
            "from": from_date,
            "sortBy": "relevancy",
            "apiKey": settings.NEWS_API_KEY,
            "language": "en"
        }

        response = await self.client.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])

        negative_count = 0
        keywords_found = set()

        for article in articles:
            content = (article.get("title", "") + " " +
                       article.get("description", "")).lower()

            for keyword in self.NEGATIVE_KEYWORDS:
                if keyword in content:
                    negative_count += 1
                    keywords_found.add(keyword)

        return NormalizedNews(
            negative_event_count=negative_count,
            keywords_found=list(keywords_found)
        )
