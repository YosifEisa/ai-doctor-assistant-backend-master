from typing import Optional
from pydantic import BaseModel, Field

from app.models.health_profile import HealthStatusEnum


class HealthProfileBase(BaseModel):
    """Base health profile schema."""
    health_status: Optional[HealthStatusEnum] = None
    activity_level: Optional[str] = Field(None, max_length=50)
    dietary_notes: Optional[str] = None
    sleep_pattern: Optional[str] = Field(None, max_length=100)


class HealthProfileCreate(HealthProfileBase):
    """Schema for creating a health profile."""
    pass


class HealthProfileRead(HealthProfileBase):
    """Schema for reading health profile data."""
    profile_id: str
    user_id: str
    
    class Config:
        from_attributes = True


class HealthProfileUpdate(HealthProfileBase):
    """Schema for updating health profile data."""
    pass
