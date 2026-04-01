from sqlalchemy import Column, Integer, String
from database.db import Base

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    balance = Column(Integer, nullable=False, default=0)
