from app.clients.llm_client import LLMClient


class InsightService:

    def __init__(self):
        self.llm_client = LLMClient()

    async def generate_ai_insight(self, response_data: dict) -> dict:
        """
        Forward the full contextual travel payload to the LLM and return
        per-section dashboard explanations + an advisory block.
        """
        structured_input = {
            "destination": response_data["destination"],
            "travel_date": response_data["travel_date"],
            "duration_days": response_data["duration_days"],
            "environment": response_data["environment"],
            "news_context": response_data["news_context"]
        }

        return await self.llm_client.generate_travel_insight(structured_input)