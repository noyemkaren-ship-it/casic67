from sqlalchemy import create_engine
from database.db import Base, engine
from models.user import User  # Импортируем модель User

def init_db():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_db()