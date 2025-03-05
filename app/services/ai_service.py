from app.providers.base_ai_provider import BaseAIProvider

class AIService:
    def __init__(self, provider: BaseAIProvider):
        self.provider = provider
    
    def generate_text(self, prompt: str) -> str:
        if not prompt or prompt.strip() == "":
            raise ValueError("Prompt cannot be empty")
        
        return self.provider.generate_text(prompt)
