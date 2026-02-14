from fastapi import APIRouter, HTTPException, status

from app.utils.dependencies import DatabaseDep, CurrentUserDep
from app.models.health_profile import HealthProfile
from app.schemas.health_profile import HealthProfileCreate, HealthProfileRead, HealthProfileUpdate

router = APIRouter(prefix="/health-profile", tags=["Health Profile / Lifestyle"])


@router.post("", response_model=HealthProfileRead, status_code=status.HTTP_201_CREATED)
def create_health_profile(
    profile_data: HealthProfileCreate,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    """Create a health profile / lifestyle information for the current user."""
    # Check if profile already exists
    existing_profile = db.query(HealthProfile).filter(
        HealthProfile.user_id == current_user.user_id
    ).first()
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Health profile already exists. Use PUT to update."
        )
    
    new_profile = HealthProfile(
        user_id=current_user.user_id,
        health_status=profile_data.health_status,
        activity_level=profile_data.activity_level,
        dietary_notes=profile_data.dietary_notes,
        sleep_pattern=profile_data.sleep_pattern,
    )
    
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    
    return new_profile


@router.get("", response_model=HealthProfileRead)
def get_health_profile(current_user: CurrentUserDep, db: DatabaseDep):
    """Get health profile / lifestyle information for the current user."""
    profile = db.query(HealthProfile).filter(
        HealthProfile.user_id == current_user.user_id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health profile not found"
        )
    
    return profile


@router.put("", response_model=HealthProfileRead)
def update_health_profile(
    profile_data: HealthProfileUpdate,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    """Update health profile / lifestyle information for the current user."""
    profile = db.query(HealthProfile).filter(
        HealthProfile.user_id == current_user.user_id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health profile not found. Use POST to create."
        )
    
    # Update only provided fields
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    
    return profile


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_health_profile(current_user: CurrentUserDep, db: DatabaseDep):
    """Delete health profile for the current user."""
    profile = db.query(HealthProfile).filter(
        HealthProfile.user_id == current_user.user_id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health profile not found"
        )
    
    db.delete(profile)
    db.commit()
    
    return None
