from app.models.internal_models import (
    NormalizedWeather,
    NormalizedAQI,
    NormalizedHoliday,
    NormalizedNews
)
from app.config import settings

class ScoringEngine:

    def __init__(self):
        self.weights = settings.RISK_WEIGHTS

    def calculate_weather_score(self, weather: NormalizedWeather):
        explanations = []

        if weather.temperature > 40:
            score = 90
            explanations.append(f"Extreme heat detected ({weather.temperature}°C).")
        elif weather.temperature > 35:
            score = 60
            explanations.append(f"High temperature detected ({weather.temperature}°C).")
        else:
            score = 10
            explanations.append("Weather conditions are within safe temperature range.")

        if weather.extreme:
            explanations.append("Extreme weather conditions reported.")

        return score, explanations

    def calculate_aqi_score(self, aqi: NormalizedAQI):
        explanations = []

        category_score_map = {
            "Good": 10,
            "Fair": 30,
            "Moderate": 60,
            "Poor": 80,
            "Very Poor": 95
        }

        score = category_score_map.get(aqi.category, 50)
        explanations.append(f"AQI category is {aqi.category}.")

        return score, explanations

    def calculate_holiday_score(self, holiday: NormalizedHoliday):
        explanations = []

        if holiday.is_holiday:
            score = 70
            explanations.append(f"Public holiday detected: {holiday.holiday_name}.")
        else:
            score = 10
            explanations.append("No major public holidays during travel period.")

        return score, explanations

    def calculate_news_score(self, news: NormalizedNews):
        explanations = []

        count = news.negative_event_count

        if count == 0:
            score = 10
            explanations.append("No recent negative news events found.")
        elif count <= 2:
            score = 40
            explanations.append("A few concerning news events reported recently.")
        elif count <= 5:
            score = 70
            explanations.append("Multiple concerning news events reported recently.")
        else:
            score = 90
            explanations.append("High number of negative news events detected.")

        for event in news.events:
            explanations.append(
                f"Reported: '{event.title}' "
                f"(Source: {event.source}, Keyword: {event.keyword_triggered})"
            )

        return score, explanations

    def calculate_total_score(
        self,
        weather: NormalizedWeather,
        aqi: NormalizedAQI,
        holiday: NormalizedHoliday,
        news: NormalizedNews
    ):
        weather_score, weather_exp = self.calculate_weather_score(weather)
        aqi_score, aqi_exp = self.calculate_aqi_score(aqi)
        holiday_score, holiday_exp = self.calculate_holiday_score(holiday)
        news_score, news_exp = self.calculate_news_score(news)

        total_score = (
            weather_score * self.weights["weather"] +
            aqi_score * self.weights["aqi"] +
            holiday_score * self.weights["holiday"] +
            news_score * self.weights["news"]
        )

        total_score = int(total_score)

        explanations = weather_exp + aqi_exp + holiday_exp + news_exp

        if total_score < 30:
            level = "Low"
        elif total_score < 60:
            level = "Moderate"
        else:
            level = "High"

        return {
            "risk_score": total_score,
            "risk_level": level,
            "factor_breakdown": {
                "weather": weather_score,
                "aqi": aqi_score,
                "holiday": holiday_score,
                "news": news_score
            },
            "explanations": explanations
        }
