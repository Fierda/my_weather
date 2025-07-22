from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base


class WeatherResponse(BaseModel):
    location: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    feels_like: float
    icon: str


class LocationRequest(BaseModel):
    city: str
    country: Optional[str] = None

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    
    SearchHistory: Mapped[list["SearchHistory"]] = relationship(
        "SearchHistory", back_populates="user"
    )
    tokens = relationship("UserToken", back_populates="user")
        
class SearchHistory(Base):
    __tablename__ = 'search_history'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    location: Mapped[str] = mapped_column(String, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    
    user: Mapped[User] = relationship("User", back_populates="SearchHistory")
    
    
class UserToken(Base):
    __tablename__ = "user_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationship
    user = relationship("User", back_populates="tokens")