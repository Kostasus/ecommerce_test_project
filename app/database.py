from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL

# Строка подключения для SQLite
DATABASE_URL_SQLITE = "sqlite:///ecommerce.db"

# Создаём Engine
engine = create_engine(DATABASE_URL_SQLITE, echo=True)

# Настраиваем фабрику сеансов
SessionLocal = sessionmaker(bind=engine)

# --------------- Асинхронное подключение к PostgreSQL -------------------------

# Создаём Engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


# Определяем базовый класс для моделей
class Base(DeclarativeBase):
    pass
