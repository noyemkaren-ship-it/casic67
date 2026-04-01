from sqlalchemy.orm import Session
from models.user import User
from database.db import SessionLocal  

class UserRepository:
    def __init__(self):
        self.db = SessionLocal()
    
    def get_all(self):
        return self.db.query(User).all()
    
    def create_user(self, name: str, password: str):
        existing_user = self.db.query(User).filter(User.name == name).first()
        if existing_user:
            return {"message": "Name is use!"}
        
        new_user = User(name=name, password=password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def patch_balance_user(self, name: str, balance: int):
        if balance > 0:
            user = self.db.query(User).filter(User.name == name).first()
            if user:
                user.balance = balance
                self.db.commit()
                self.db.refresh(user)
                return user
        return {"message": "404 user not found"}
    
    def get_by_name(self, name: str):
        result = self.db.query(User).filter(User.name == name).first()
        return result
    
    
    def login(self, name: str, password: str):
        result = self.db.query(User).where(User.name == name, User.password == password).first()
        return result is not None

    def close(self):
        self.db.close()