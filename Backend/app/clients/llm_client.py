import json
import asyncio
import logging
from groq import Groq
from app.config import settings

logger = logging.getLogger(__name__)


class LLMClient:

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def _call_groq(self, prompt: str) -> str:
        """Synchronous Groq call — offloaded to a thread pool."""
        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional travel analyst. "
                        "You interpret real-time destination data and provide "
                        "clear, practical insights to help travellers make informed decisions. "
                        "Use only the data provided. Never invent facts."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return completion.choices[0].message.content

    async def generate_travel_insight(self, structured_data: dict) -> dict:
        try:
            prompt = f"""
You are a professional travel analyst. Analyse the destination data below and generate
clear, honest, and practical travel insights for each section of the travel dashboard.

RULES:
- Use ONLY the data provided. Do NOT invent facts or add external knowledge.
- Return ONLY raw JSON. No markdown, no code fences, no extra commentary.
- weather_explanation and air_quality_explanation: 1-2 sentences referencing actual values.
- news_explanation: reference actual event count and keywords if events exist; be reassuring if count is 0.
- advisory: 2-3 sentences overall travel advisory that synthesises all the data above.
- precautions: list of 3-5 specific, actionable precaution strings.
- tips: list of 3-5 practical journey tip strings.

INPUT DATA:
{json.dumps(structured_data, indent=2)}

OUTPUT FORMAT (fill every key, do not omit any):
{{
  "weather_explanation": "...",
  "air_quality_explanation": "...",
  "news_explanation": "...",
  "advisory": "...",
  "precautions": [
    "...",
    "...",
    "..."
  ],
  "tips": [
    "...",
    "...",
    "..."
  ]
}}
"""

            response_text = await asyncio.to_thread(self._call_groq, prompt)
            response_text = response_text.strip()

            # Safely extract the JSON object from the response
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            json_part = response_text[start:end]

            return json.loads(json_part)

        except Exception as e:
            logger.error(f"LLM insight generation failed: {e}", exc_info=True)
            return {
                "weather_explanation": "Weather analysis currently unavailable.",
                "air_quality_explanation": "Air quality analysis currently unavailable.",
                "news_explanation": "News analysis currently unavailable.",
                "advisory": "AI advisory currently unavailable. Please check local sources before travelling.",
                "precautions": [],
                "tips": []
            }