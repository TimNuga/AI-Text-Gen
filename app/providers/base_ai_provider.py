class BaseAIProvider:
    def generate_text(self, prompt: str) -> str:
        """
        Method to generate text from a prompt.
        Subclasses should override this.
        """
        raise NotImplementedError("Subclasses must implement generate_text()")
