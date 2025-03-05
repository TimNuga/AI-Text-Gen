import logging
from app.providers.base_ai_provider import BaseAIProvider

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, provider: BaseAIProvider):
        self.provider = provider
    
    def generate_text(self, prompt: str) -> str:
        if not prompt or prompt.strip() == "":
            raise ValueError("Prompt cannot be empty")
        
        logger.info("Sending prompt to provider: %s", prompt)
        result = self.provider.generate_text(prompt)
        logger.info("Received generated text: %s", result)
        return result
