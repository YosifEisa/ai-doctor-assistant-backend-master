from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class ChronicDiseaseBase(BaseModel):
    """Base chronic disease schema."""
    name: str = Field(..., min_length=1, max_length=200)
    diagnosis_date: Optional[date] = None


class ChronicDiseaseCreate(ChronicDiseaseBase):
    """Schema for creating a chronic disease record."""
    pass


class ChronicDiseaseRead(ChronicDiseaseBase):
    """Schema for reading chronic disease data."""
    disease_id: str
    user_id: str
    
    class Config:
        from_attributes = True
