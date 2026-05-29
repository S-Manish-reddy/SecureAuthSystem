from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from backend.database.db import get_db

from backend.models.user_model import User

from backend.auth.jwt_handler import verify_access_token

from backend.security.two_factor import generate_2fa_secret
from backend.security.two_factor import generate_otp_uri
from backend.security.two_factor import generate_qr_code
from backend.security.two_factor import verify_otp

router = APIRouter()

security = HTTPBearer()


@router.get("/profile")
def get_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return {
        "message": "Protected profile accessed",
        "user_data": payload
    }


@router.post("/enable-2fa")
def enable_2fa(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = payload.get("user_id")

    existing_user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not existing_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    secret = generate_2fa_secret()

    existing_user.two_factor_secret = secret

    db.commit()

    otp_uri = generate_otp_uri(
        existing_user.email,
        secret
    )

    qr_path = f"backend/logs/{existing_user.id}_qr.png"

    generate_qr_code(
        otp_uri,
        qr_path
    )

    return {
        "message": "2FA enabled",
        "secret": secret,
        "qr_code_path": qr_path
    }


@router.post("/verify-2fa")
def verify_two_factor(
    otp: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = payload.get("user_id")

    existing_user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not existing_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    valid_otp = verify_otp(
        existing_user.two_factor_secret,
        otp
    )

    if not valid_otp:

        raise HTTPException(
            status_code=401,
            detail="Invalid OTP"
        )

    existing_user.two_factor_enabled = True

    db.commit()

    return {
        "message": "2FA verification successful"
    }