import logging
from openai import OpenAI
from app.config import Config
from app.providers.base_ai_provider import BaseAIProvider

logger = logging.getLogger(__name__)

class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def generate_text(self, prompt: str) -> str:
        logger.info("Received prompt: %s", prompt)
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            logger.debug("Raw API response: %s", response)
            
            result = response.choices[0].message.content.strip()
            logger.info("Generated text: %s", result)
            return result
        except Exception as e:
            logger.exception("Error during text generation")
            raise e
