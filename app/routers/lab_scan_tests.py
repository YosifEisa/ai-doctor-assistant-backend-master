from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query

from app.utils.dependencies import DatabaseDep, CurrentUserDep
from app.models.lab_scan_test import LabScanTest, TestTypeEnum
from app.schemas.lab_scan_test import LabScanTestCreate, LabScanTestRead

router = APIRouter(prefix="/tests", tags=["Lab & Scan Tests"])


@router.post("", response_model=LabScanTestRead, status_code=status.HTTP_201_CREATED)
def create_test(
    test_data: LabScanTestCreate,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    """Register a new lab or scan test for the current user.
    
    Specify the test_type as 'Lab' or 'Scan'.
    """
    new_test = LabScanTest(
        user_id=current_user.user_id,
        test_type=test_data.test_type,
        image_url=test_data.image_url,
    )

    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    return new_test


@router.get("", response_model=List[LabScanTestRead])
def get_tests(
    current_user: CurrentUserDep,
    db: DatabaseDep,
    test_type: Optional[TestTypeEnum] = Query(None, description="Filter by test type (Lab or Scan)")
):
    """Retrieve all tests for the current user, optionally filtered by type."""
    query = db.query(LabScanTest).filter(LabScanTest.user_id == current_user.user_id)

    if test_type:
        query = query.filter(LabScanTest.test_type == test_type)

    tests = query.order_by(LabScanTest.created_at.desc()).all()
    return tests


@router.get("/{test_id}", response_model=LabScanTestRead)
def get_test(
    test_id: str,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    """Get a specific test."""
    test = db.query(LabScanTest).filter(
        LabScanTest.test_id == test_id,
        LabScanTest.user_id == current_user.user_id
    ).first()

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )

    return test


@router.delete("/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test(
    test_id: str,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    """Delete a test record."""
    test = db.query(LabScanTest).filter(
        LabScanTest.test_id == test_id,
        LabScanTest.user_id == current_user.user_id
    ).first()

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )

    db.delete(test)
    db.commit()

    return None
