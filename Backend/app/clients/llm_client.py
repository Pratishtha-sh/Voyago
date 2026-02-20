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
        """Synchronous Groq call — runs in a thread pool via asyncio.to_thread."""
        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a precise travel analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return completion.choices[0].message.content

    async def generate_travel_insight(self, structured_data: dict) -> dict:
        try:
            prompt = f"""
You are a professional travel safety and advisory analyst.

Use ONLY the provided structured data.
Do NOT invent new information.
Do NOT add external facts.
Return ONLY raw JSON.
Do NOT include explanations.
Do NOT include markdown.
Do NOT wrap in code blocks.

INPUT DATA:
{json.dumps(structured_data, indent=2)}

OUTPUT FORMAT:
{{
  "summary": "",
  "precautions": [],
  "travel_advice": "",
  "best_time_suggestion": ""
}}
"""

            # Groq SDK is synchronous — offload to a thread to avoid blocking the event loop
            response_text = await asyncio.to_thread(self._call_groq, prompt)
            response_text = response_text.strip()

            # Extract JSON part safely
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            json_part = response_text[start:end]

            return json.loads(json_part)

        except Exception as e:
            logger.error(f"LLM insight generation failed: {e}", exc_info=True)
            # Fail gracefully
            return {
                "summary": "AI insight currently unavailable.",
                "precautions": [],
                "travel_advice": "",
                "best_time_suggestion": ""
            }