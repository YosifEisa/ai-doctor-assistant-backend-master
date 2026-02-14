from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class MedicationBase(BaseModel):
    """Base medication schema."""
    med_name: str = Field(..., min_length=1, max_length=200)
    dose: Optional[str] = Field(None, max_length=50)
    frequency: Optional[str] = Field(None, max_length=100)
    duration_end: Optional[date] = None


class MedicationCreate(MedicationBase):
    """Schema for creating a medication record."""
    pass


class MedicationRead(MedicationBase):
    """Schema for reading medication data."""
    med_id: str
    user_id: str
    
    class Config:
        from_attributes = True


class MedicationUpdate(BaseModel):
    """Schema for updating medication data."""
    med_name: Optional[str] = Field(None, min_length=1, max_length=200)
    dose: Optional[str] = Field(None, max_length=50)
    frequency: Optional[str] = Field(None, max_length=100)
    duration_end: Optional[date] = None
