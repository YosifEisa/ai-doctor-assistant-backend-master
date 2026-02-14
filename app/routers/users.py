from fastapi import APIRouter, HTTPException, status

from app.utils.dependencies import DatabaseDep, CurrentUserDep
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
def get_current_user_profile(current_user: CurrentUserDep):
    """Get the current authenticated user's profile."""
    return current_user


@router.put("/me", response_model=UserRead)
def update_current_user(
    user_data: UserUpdate,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    """Update the current authenticated user's information."""
    # Update only provided fields
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(current_user: CurrentUserDep, db: DatabaseDep):
    """Delete the current authenticated user's account."""
    db.delete(current_user)
    db.commit()
    
    return None
