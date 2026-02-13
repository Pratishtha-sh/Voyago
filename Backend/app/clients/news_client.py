from datetime import datetime, timedelta
from app.config import settings
from app.clients.base_client import BaseClient
from app.models.internal_models import NormalizedNews, NewsEvent


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
        "disaster",
        "attack",
        "terror"
    ]

    async def get_news_risk(self, city: str):
        from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

        params = {
            "q": city,
            "from": from_date,
            "sortBy": "relevancy",
            "apiKey": settings.NEWS_API_KEY,
            "language": "en",
            "pageSize": 20
        }

        response = await self.client.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])

        events = []

        for article in articles:
            content = (
                (article.get("title") or "") + " " +
                (article.get("description") or "")
            ).lower()

            for keyword in self.NEGATIVE_KEYWORDS:
                if keyword in content:
                    events.append(
                        NewsEvent(
                            title=article.get("title", "No title"),
                            source=article.get("source", {}).get("name", "Unknown"),
                            url=article.get("url", ""),
                            published_at=article.get("publishedAt", ""),
                            keyword_triggered=keyword
                        )
                    )
                    break  # Avoid double-counting same article

            if len(events) >= 5:
                break  # Limit evidence size

        return NormalizedNews(
            negative_event_count=len(events),
            events=events
        )
