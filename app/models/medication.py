import uuid
from datetime import date
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.orm import relationship

from app.database import Base


class Medication(Base):
    """Medication model."""
    
    __tablename__ = "medications"
    
    med_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    med_name = Column(String(200), nullable=False)
    dose = Column(String(50), nullable=True)  # e.g., 500mg
    frequency = Column(String(100), nullable=True)  # e.g., "2 times per day"
    duration_end = Column(Date, nullable=True)  # "Until when"
    
    # Relationship
    user = relationship("User", back_populates="medications")
