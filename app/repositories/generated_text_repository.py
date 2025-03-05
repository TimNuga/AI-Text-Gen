from app.models import GeneratedText

class GeneratedTextRepository:
    def __init__(self, session):
        self.session = session
    
    def create_text(self, user_id: int, prompt: str, response: str) -> GeneratedText:
        gt = GeneratedText(user_id=user_id, prompt=prompt, response=response)
        self.session.add(gt)
        self.session.commit()
        return gt

    def find_by_id(self, text_id: int) -> GeneratedText:
        return self.session.query(GeneratedText).get(text_id)
    
    def update_text(self, gen_text: GeneratedText, new_prompt: str = None, new_response: str = None):
        if new_prompt:
            gen_text.prompt = new_prompt
        if new_response:
            gen_text.response = new_response
        self.session.commit()
        return gen_text
    
    def delete_text(self, gen_text: GeneratedText):
        self.session.delete(gen_text)
        self.session.commit()
