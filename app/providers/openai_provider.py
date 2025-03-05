from openai import OpenAI
from app.config import Config
from app.providers.base_ai_provider import BaseAIProvider

class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        self.client = OpenAI(api_key = Config.OPENAI_API_KEY)
    
    def generate_text(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            result = response.choices[0].message.content.strip()
        except Exception as e:
            raise e
