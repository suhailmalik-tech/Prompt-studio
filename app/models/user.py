from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey 
from sqlalchemy.orm import relationship
from datetime import datetime , timezone
from app.core.db import Base


class User(Base):
    __tablename__ = "users"
    id =  Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

prompts = relationship("Prompt", back_populates="owner", cascade="all, delete-orphan")