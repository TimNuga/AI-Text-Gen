from passlib.hash import bcrypt
from app.repositories.user_repository import UserRepository
from app.models import User

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def register_user(self, username: str, password: str):
        exists = self.user_repo.find_by_username(username)
        if exists:
            raise ValueError("User already exists")
        
        password_hash = bcrypt.hash(password)
        new_user = self.user_repo.create_user(username, password_hash)
        return new_user
    
    def verify_credentials(self, username: str, password: str) -> User:
        user = self.user_repo.find_by_username(username)
        if not user:
            return None
        if not bcrypt.verify(password, user.password_hash):
            return None
        return user
