import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.orm import relationship

from app.database import Base


class Allergy(Base):
    """Allergy model."""
    
    __tablename__ = "allergies"
    
    allergy_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    allergy_name = Column(String(200), nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="allergies")
