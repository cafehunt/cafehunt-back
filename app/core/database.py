from typing import Any

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./cafe.db"


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base: Any = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    orders = relationship("Order", back_populates="user")
