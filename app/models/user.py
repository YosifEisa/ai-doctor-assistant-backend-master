import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.orm import relationship

from app.database import Base


class GenderEnum(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class User(Base):
    """User account model."""
    
    __tablename__ = "users"
    
    user_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code_number = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    passport_id = Column(String(50), nullable=False)
    gender = Column(SQLEnum(GenderEnum), nullable=False)
    nationality = Column(String(100), nullable=True)
    marital_status = Column(String(50), nullable=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    otp_code = Column(String(10), nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    health_profile = relationship("HealthProfile", back_populates="user", uselist=False)
    family_members = relationship("FamilyMember", back_populates="user", cascade="all, delete-orphan", foreign_keys="FamilyMember.user_id")
    chronic_diseases = relationship("ChronicDisease", back_populates="user", cascade="all, delete-orphan")
    allergies = relationship("Allergy", back_populates="user", cascade="all, delete-orphan")
    lab_scan_tests = relationship("LabScanTest", back_populates="user", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="user", cascade="all, delete-orphan")
