from typing import List
from fastapi import APIRouter, HTTPException, status

from app.utils.dependencies import DatabaseDep, CurrentUserDep
from app.models.user import User
from app.models.family_member import FamilyMember
from app.schemas.family_member import FamilyMemberCreate, FamilyMemberRead

router = APIRouter(prefix="/family-members", tags=["Family Members"])


def build_family_member_response(member: FamilyMember, db) -> dict:
    """Build response with linked user's name and code_number."""
    linked_user = db.query(User).filter(User.user_id == member.linked_user_id).first()
    
    return {
        "family_id": member.family_id,
        "user_id": member.user_id,
        "name": f"{linked_user.first_name} {linked_user.last_name}" if linked_user else member.name,
        "relation": member.relation,
        "linked_user_id": member.linked_user_id,
        "linked_user_code_number": linked_user.code_number if linked_user else None,
    }


@router.post("", response_model=FamilyMemberRead, status_code=status.HTTP_201_CREATED)
def create_family_member(
    member_data: FamilyMemberCreate,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    """Register a new family member for the current user.
    
    The family member must be an existing registered user.
    Their name is automatically retrieved from their profile.
    """
    # Look up the user by code_number (required)
    linked_user = db.query(User).filter(
        User.code_number == member_data.linked_user_code_number
    ).first()
    
    if not linked_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No registered user found with code number: {member_data.linked_user_code_number}"
        )
    
    # Prevent linking to self
    if linked_user.user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add yourself as a family member"
        )
    
    # Check if this family member is already added
    existing = db.query(FamilyMember).filter(
        FamilyMember.user_id == current_user.user_id,
        FamilyMember.linked_user_id == linked_user.user_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user is already added as a family member"
        )
    
    # Get name from linked user's profile
    name = f"{linked_user.first_name} {linked_user.last_name}"
    
    new_member = FamilyMember(
        user_id=current_user.user_id,
        name=name,
        relation=member_data.relation,
        linked_user_id=linked_user.user_id,
    )
    
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    return build_family_member_response(new_member, db)


@router.get("", response_model=List[FamilyMemberRead])
def get_family_members(current_user: CurrentUserDep, db: DatabaseDep):
    """Retrieve all family members for the current user."""
    members = db.query(FamilyMember).filter(
        FamilyMember.user_id == current_user.user_id
    ).all()
    return [build_family_member_response(m, db) for m in members]


@router.get("/{family_id}", response_model=FamilyMemberRead)
def get_family_member(
    family_id: str,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    """Get a specific family member."""
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == current_user.user_id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found"
        )
    
    return build_family_member_response(member, db)


@router.delete("/{family_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_family_member(
    family_id: str,
    current_user: CurrentUserDep,
    db: DatabaseDep,
):
    """Delete a family member."""
    member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == current_user.user_id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found"
        )
    
    db.delete(member)
    db.commit()
    
    return None
