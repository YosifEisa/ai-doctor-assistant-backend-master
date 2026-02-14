from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.utils.dependencies import DatabaseDep
from app.utils.security import (
    hash_password,
    verify_password,
    generate_otp,
    get_otp_expiry,
    is_otp_valid,
    generate_code_number,
    create_access_token,
)
from app.models.user import User
from app.schemas.user import (
    UserRegister,
    UserRead,
    Token,
    ForgotPasswordRequest,
    VerifyOTPRequest,
    ChangePasswordRequest,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DatabaseDep,
):
    user = db.query(User).filter(User.phone_number == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.user_id)}
    )
    return Token(access_token=access_token)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db: DatabaseDep):
    """Register a new user account."""

    if db.query(User).filter(User.phone_number == user_data.phone_number).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

    if db.query(User).filter(User.passport_id == user_data.passport_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passport ID already registered"
        )

    try:
        new_user = User(
            code_number=generate_code_number(),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            passport_id=user_data.passport_id,
            gender=user_data.gender,
            nationality=user_data.nationality,
            marital_status=user_data.marital_status,
            phone_number=user_data.phone_number,
            password_hash=hash_password(user_data.password),
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )



@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(request: ForgotPasswordRequest, db: DatabaseDep):
    print("ALL USERS IN DB:", db.query(User).all())

    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    otp = generate_otp()
    user.otp_code = otp
    user.otp_expiry = get_otp_expiry()

    db.commit()

    return {
        "message": "OTP sent successfully",
        "otp": otp
    }




@router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(request: VerifyOTPRequest, db: DatabaseDep):
    """Verify an OTP code."""
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not is_otp_valid(user.otp_expiry):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired"
        )

    if user.otp_code != request.otp_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP code"
        )

    return {"message": "OTP verified successfully", "valid": True}


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(request: ChangePasswordRequest, db: DatabaseDep):
    """Change password using OTP verification."""
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not is_otp_valid(user.otp_expiry):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired"
        )

    if user.otp_code != request.otp_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP code"
        )

    user.password_hash = hash_password(request.new_password)
    user.otp_code = None
    user.otp_expiry = None

    db.commit()

    return {"message": "password changed successfully"}
