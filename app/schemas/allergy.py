from pydantic import BaseModel, Field


class AllergyBase(BaseModel):
    """Base allergy schema."""
    allergy_name: str = Field(..., min_length=1, max_length=200)


class AllergyCreate(AllergyBase):
    """Schema for creating an allergy record."""
    pass


class AllergyRead(AllergyBase):
    """Schema for reading allergy data."""
    allergy_id: str
    user_id: str
    
    class Config:
        from_attributes = True
