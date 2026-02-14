import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.orm import relationship

from app.database import Base


class FamilyMember(Base):
    """Family member model."""
    
    __tablename__ = "family_members"
    
    family_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    relation = Column(String(50), nullable=False)  # e.g., Spouse, Child, Parent
    
    # Optional: Link to an existing user in the system (identified by code_number during creation)
    linked_user_id = Column(CHAR(36), ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Relationships
    user = relationship("User", back_populates="family_members", foreign_keys=[user_id])
    linked_user = relationship("User", foreign_keys=[linked_user_id])
