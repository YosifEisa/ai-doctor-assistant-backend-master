from typing import List
from fastapi import APIRouter, HTTPException, status

from app.utils.dependencies import DatabaseDep, CurrentUserDep
from app.utils.security import encrypt_text, decrypt_text
from app.models.chronic_disease import ChronicDisease
from app.schemas.chronic_disease import (
    ChronicDiseaseCreate,
    ChronicDiseaseRead,
)

router = APIRouter(prefix="/diseases", tags=["Chronic & Genetic Diseases"])


@router.post("", response_model=ChronicDiseaseRead, status_code=status.HTTP_201_CREATED)
def create_disease(
    disease_data: ChronicDiseaseCreate,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    new_disease = ChronicDisease(
        user_id=current_user.user_id,
        name_encrypted=encrypt_text(disease_data.name),
        diagnosis_date=disease_data.diagnosis_date,
    )

    db.add(new_disease)
    db.commit()
    db.refresh(new_disease)

    new_disease.name = decrypt_text(new_disease.name_encrypted)
    return new_disease


@router.get("", response_model=List[ChronicDiseaseRead])
def get_diseases(current_user: CurrentUserDep, db: DatabaseDep):
    diseases = db.query(ChronicDisease).filter(
        ChronicDisease.user_id == current_user.user_id
    ).all()

    for d in diseases:
        d.name = decrypt_text(d.name_encrypted)

    return diseases


@router.get("/{disease_id}", response_model=ChronicDiseaseRead)
def get_disease(
    disease_id: str,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    disease = db.query(ChronicDisease).filter(
        ChronicDisease.disease_id == disease_id,
        ChronicDisease.user_id == current_user.user_id,
    ).first()

    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disease not found",
        )

    disease.name = decrypt_text(disease.name_encrypted)
    return disease


@router.delete("/{disease_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_disease(
    disease_id: str,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    disease = db.query(ChronicDisease).filter(
        ChronicDisease.disease_id == disease_id,
        ChronicDisease.user_id == current_user.user_id,
    ).first()

    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disease not found",
        )

    db.delete(disease)
    db.commit()
    return None
