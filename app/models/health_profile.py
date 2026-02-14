import uuid
import enum
from sqlalchemy import Column, String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.orm import relationship

from app.database import Base


class HealthStatusEnum(str, enum.Enum):
    HEALTHY = "Healthy"
    CHECKUP = "Checkup"
    CRITICAL = "Critical"


class HealthProfile(Base):
    """Health profile / lifestyle information model."""
    
    __tablename__ = "health_profiles"
    
    profile_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    health_status = Column(SQLEnum(HealthStatusEnum), nullable=True)
    activity_level = Column(String(50), nullable=True)  # e.g., Sedentary, Active
    dietary_notes = Column(Text, nullable=True)
    sleep_pattern = Column(String(100), nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="health_profile")
