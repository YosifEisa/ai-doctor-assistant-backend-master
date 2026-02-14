from typing import List
from fastapi import APIRouter, HTTPException, status

from app.utils.dependencies import DatabaseDep, CurrentUserDep
from app.models.allergy import Allergy
from app.schemas.allergy import AllergyCreate, AllergyRead

router = APIRouter(prefix="/allergies", tags=["Allergies"])


@router.post("", response_model=AllergyRead, status_code=status.HTTP_201_CREATED)
def create_allergy(
    allergy_data: AllergyCreate,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    """Register a new allergy for the current user."""
    new_allergy = Allergy(
        user_id=current_user.user_id,
        allergy_name=allergy_data.allergy_name,
    )
    
    db.add(new_allergy)
    db.commit()
    db.refresh(new_allergy)
    
    return new_allergy


@router.get("", response_model=List[AllergyRead])
def get_allergies(current_user: CurrentUserDep, db: DatabaseDep):
    """Retrieve all allergies for the current user."""
    allergies = db.query(Allergy).filter(
        Allergy.user_id == current_user.user_id
    ).all()
    return allergies


@router.get("/{allergy_id}", response_model=AllergyRead)
def get_allergy(
    allergy_id: str,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    """Get a specific allergy."""
    allergy = db.query(Allergy).filter(
        Allergy.allergy_id == allergy_id,
        Allergy.user_id == current_user.user_id
    ).first()
    
    if not allergy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allergy not found"
        )
    
    return allergy


@router.delete("/{allergy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_allergy(
    allergy_id: str,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    """Delete an allergy."""
    allergy = db.query(Allergy).filter(
        Allergy.allergy_id == allergy_id,
        Allergy.user_id == current_user.user_id
    ).first()
    
    if not allergy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allergy not found"
        )
    
    db.delete(allergy)
    db.commit()
    
    return None
