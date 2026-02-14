from typing import Optional
from pydantic import BaseModel, Field


class FamilyMemberCreate(BaseModel):
    """Schema for creating a family member.
    
    The family member must be an existing registered user.
    Their name is automatically retrieved from their profile.
    """
    linked_user_code_number: str = Field(
        ..., 
        description="Code number of the registered user to add as family member"
    )
    relation: str = Field(..., min_length=1, max_length=50)


class FamilyMemberRead(BaseModel):
    """Schema for reading family member data."""
    family_id: str
    user_id: str
    name: str  # Retrieved from linked user's first_name + last_name
    relation: str
    linked_user_id: str
    linked_user_code_number: str
    
    class Config:
        from_attributes = True
