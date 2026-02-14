import random
import string
from datetime import datetime, timedelta, timezone
from typing import Any
import os

from jose import jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet

from app.config import settings


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """Hash a password using Argon2."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its Argon2 hash."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_otp(length: int = 6) -> str:
    """Generate a random numeric OTP code."""
    return "".join(random.choices(string.digits, k=length))


def get_otp_expiry() -> datetime:
    """Get OTP expiry time."""
    return datetime.now(timezone.utc) + timedelta(
        minutes=settings.OTP_EXPIRY_MINUTES
    )


def is_otp_valid(otp_expiry: datetime | None) -> bool:
    if otp_expiry is None:
        return False
    if otp_expiry.tzinfo is None:
        otp_expiry = otp_expiry.replace(tzinfo=timezone.utc)

    return datetime.now(timezone.utc) < otp_expiry



def generate_code_number() -> str:
    """Generate a unique public code number for a user."""
    prefix = "USR"
    random_part = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=8)
    )
    return f"{prefix}-{random_part}"



FERNET_KEY = os.getenv("FERNET_KEY")

if not FERNET_KEY:
    FERNET_KEY = Fernet.generate_key()

fernet = Fernet(FERNET_KEY)


def encrypt_text(value: str) -> str:
    """Encrypt sensitive text data."""
    return fernet.encrypt(value.encode()).decode()


def decrypt_text(value: str) -> str:
    """Decrypt sensitive text data."""
    return fernet.decrypt(value.encode()).decode()
