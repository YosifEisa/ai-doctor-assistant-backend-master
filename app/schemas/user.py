from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.user import GenderEnum


class UserBase(BaseModel):
    """Base user schema with common fields."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    passport_id: str = Field(..., min_length=1, max_length=50)
    gender: GenderEnum
    nationality: Optional[str] = Field(None, max_length=100)
    marital_status: Optional[str] = Field(None, max_length=50)
    phone_number: str = Field(..., min_length=1, max_length=20)


class UserRegister(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=6, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a user (internal use)."""
    code_number: str = Field(..., min_length=1, max_length=50)
    password_hash: str


class UserRead(UserBase):
    """Schema for reading user data."""
    user_id: str
    code_number: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user data."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    nationality: Optional[str] = Field(None, max_length=100)
    marital_status: Optional[str] = Field(None, max_length=50)


class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password request."""
    phone_number: str = Field(..., min_length=1, max_length=20)


class VerifyOTPRequest(BaseModel):
    """Schema for OTP verification."""
    phone_number: str = Field(..., min_length=1, max_length=20)
    otp_code: str = Field(..., min_length=4, max_length=10)


class ChangePasswordRequest(BaseModel):
    """Schema for changing password."""
    phone_number: str = Field(..., min_length=1, max_length=20)
    otp_code: str = Field(..., min_length=4, max_length=10)
    new_password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""
    phone_number: str = Field(..., min_length=1, max_length=20)
    password: str = Field(..., min_length=1)


class Token(BaseModel):
    """Schema for access token response."""
    access_token: str
    token_type: str = "bearer"
