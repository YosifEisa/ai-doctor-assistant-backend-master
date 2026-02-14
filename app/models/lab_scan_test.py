import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.orm import relationship

from app.database import Base


class TestTypeEnum(str, enum.Enum):
    LAB = "Lab"
    SCAN = "Scan"


class LabScanTest(Base):
    """Lab and scan tests model."""
    
    __tablename__ = "lab_scan_tests"
    
    test_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    test_type = Column(SQLEnum(TestTypeEnum), nullable=False)
    image_url = Column(String(500), nullable=True)  # Path to stored file
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="lab_scan_tests")
