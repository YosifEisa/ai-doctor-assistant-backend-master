from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.lab_scan_test import TestTypeEnum


class LabScanTestBase(BaseModel):
    """Base lab/scan test schema."""
    test_type: TestTypeEnum
    image_url: Optional[str] = Field(None, max_length=500)


class LabScanTestCreate(LabScanTestBase):
    """Schema for creating a lab/scan test record."""
    pass


class LabScanTestRead(LabScanTestBase):
    """Schema for reading lab/scan test data."""
    test_id: str
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
