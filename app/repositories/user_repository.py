from app.models import User

class UserRepository:
    def __init__(self, session):
        self.session = session

    def find_by_id(self, user_id: int) -> User:
        return self.session.query(User).get(user_id)
    
    def find_by_username(self, username: str) -> User:
        lower = username.lower()
        return self.session.query(User).filter_by(username=lower).first()
    
    def create_user(self, username: str, password_hash: str) -> User:
        # Always store in lowercase
        lower_username = username.lower()
        user = User(username=lower_username, password_hash=password_hash)
        self.session.add(user)
        self.session.commit()
        return user