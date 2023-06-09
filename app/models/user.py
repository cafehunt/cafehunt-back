from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True,  nullable=False)
    hashed_password = Column(String,   nullable=False)
    first_name = Column(String,  nullable=False)
    last_name = Column(String,  nullable=False)
    is_active = Column(Boolean,  default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean,  default=False)
    orders = relationship("Order", back_populates="user")  # orders will be created further
