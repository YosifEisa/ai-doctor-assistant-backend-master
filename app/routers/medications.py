from typing import List
from fastapi import APIRouter, HTTPException, status

from app.utils.dependencies import DatabaseDep, CurrentUserDep
from app.models.medication import Medication
from app.schemas.medication import (
    MedicationCreate,
    MedicationRead,
    MedicationUpdate,
)

router = APIRouter(prefix="/medications", tags=["Medications"])


@router.post("", response_model=MedicationRead, status_code=status.HTTP_201_CREATED)
def create_medication(
    med_data: MedicationCreate,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    new_medication = Medication(
        user_id=current_user.user_id,
        med_name=med_data.med_name,
        dose=med_data.dose,
        frequency=med_data.frequency,
        duration_end=med_data.duration_end,
    )

    db.add(new_medication)
    db.commit()
    db.refresh(new_medication)

    return new_medication


@router.get("", response_model=List[MedicationRead])
def get_medications(current_user: CurrentUserDep, db: DatabaseDep):
    return db.query(Medication).filter(
        Medication.user_id == current_user.user_id
    ).all()


@router.get("/{med_id}", response_model=MedicationRead)
def get_medication(
    med_id: str,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    medication = db.query(Medication).filter(
        Medication.med_id == med_id,
        Medication.user_id == current_user.user_id
    ).first()

    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medication not found"
        )

    return medication


@router.put("/{med_id}", response_model=MedicationRead)
def update_medication(
    med_id: str,
    med_data: MedicationUpdate,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    medication = db.query(Medication).filter(
        Medication.med_id == med_id,
        Medication.user_id == current_user.user_id
    ).first()

    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medication not found"
        )

    update_data = med_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(medication, field, value)

    db.commit()
    db.refresh(medication)

    return medication


@router.delete("/{med_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medication(
    med_id: str,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    medication = db.query(Medication).filter(
        Medication.med_id == med_id,
        Medication.user_id == current_user.user_id
    ).first()

    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medication not found"
        )

    db.delete(medication)
    db.commit()
    return None
