from app.clients.llm_client import LLMClient


class InsightService:

    def __init__(self):
        self.llm_client = LLMClient()

    async def generate_ai_insight(self, response_data: dict):
        # Pass only relevant structured data
        structured_input = {
            "destination": response_data["destination"],
            "risk_analysis": response_data["risk_analysis"],
            "explanations": response_data["explanations"]
        }

        return await self.llm_client.generate_travel_insight(structured_input)