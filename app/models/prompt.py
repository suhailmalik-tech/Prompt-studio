from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.db import Base



class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


    versions = relationship("PromptVersion", back_populates="prompt", cascade="all, delete-orphan")

class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner= relationship("User", back_populates="prompts")
    prompt_id = Column(Integer,ForeignKey("prompts.id"),nullable=False)
    raw_text = Column(Text, nullable=False)
    optimized_text=Column(Text, nullable=False)
    original_token_count=Column(Integer, nullable=False)
    optimized_token_count=Column(Integer, nullable=False)
    compression_ratio=Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    prompt = relationship("Prompt", back_populates="versions")
