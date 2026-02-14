import uuid
from datetime import date
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.orm import relationship

from app.database import Base


class ChronicDisease(Base):
    """Chronic and genetic diseases model."""
    
    __tablename__ = "chronic_diseases"
    
    disease_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    diagnosis_date = Column(Date, nullable=True)
    

    user = relationship("User", back_populates="chronic_diseases")
