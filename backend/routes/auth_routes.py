from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request

from sqlalchemy.orm import Session

from backend.database.db import get_db

from backend.models.user_model import User

from backend.schemas.user_schema import UserRegister
from backend.schemas.user_schema import UserLogin

from backend.auth.hashing import hash_password
from backend.auth.hashing import verify_password

from backend.auth.jwt_handler import create_access_token
from backend.auth.jwt_handler import create_refresh_token
from backend.auth.jwt_handler import verify_access_token

from backend.security.rate_limiter import limiter

from backend.utils.logger import security_logger

from backend.security.input_validator import sanitize_input
from backend.security.security_events import log_security_event

router = APIRouter()


@router.post("/register")
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    existing_username = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    hashed_pw = hash_password(
        user.password
    )

    new_user = User(
        username=sanitize_input(user.username),
        email=sanitize_input(user.email),
        hashed_password=hashed_pw
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    security_logger.info(
        f"New user registered: {user.email}"
    )

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
@limiter.limit("5/minute")
def login_user(
    request: Request,
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:

        security_logger.warning(
            f"Failed login attempt for email: {user.email}"
        )
        log_security_event(
            db=db,
            event_type="FAILED_LOGIN",
            user_email=user.email,
            ip_address=request.client.host,
            description="Failed login attempt for non-existing user"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if existing_user.account_locked:

        security_logger.critical(
            f"Login attempt on locked account: {user.email}"
        )

        raise HTTPException(
            status_code=403,
            detail="Account is locked"
        )

    password_valid = verify_password(
        user.password,
        existing_user.hashed_password
    )

    if not password_valid:

        existing_user.failed_login_attempts += 1

        security_logger.warning(
            f"Invalid password attempt for: {user.email}"
        )
        log_security_event(
            db=db,
            event_type="INVALID_PASSWORD",
            user_email=user.email,
            ip_address=request.client.host,
            description="Invalid password entered"
        )

        if existing_user.failed_login_attempts >= 5:

            existing_user.account_locked = True

            security_logger.critical(
                f"Account locked due to multiple failed attempts: {user.email}"
            )
            log_security_event(
            db=db,
            event_type="ACCOUNT_LOCKED",
            user_email=user.email,
            ip_address=request.client.host,
            description="Account locked after multiple failed login attempts"
            )

        db.commit()

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    existing_user.failed_login_attempts = 0

    access_token = create_access_token(
        data={
            "sub": existing_user.email,
            "user_id": existing_user.id
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": existing_user.email,
            "user_id": existing_user.id
        }
    )

    existing_user.refresh_token = refresh_token

    db.commit()
    
    log_security_event(
    db=db,
    event_type="SUCCESSFUL_LOGIN",
    user_email=user.email,
    ip_address=request.client.host,
    description="User logged in successfully"
    )

    security_logger.info(
        f"Successful login: {user.email}"
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_user.refresh_token = None

    db.commit()

    security_logger.info(
        f"User logged out: {user.email}"
    )

    return {
        "message": "Logged out successfully"
    }


@router.post("/refresh")
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):

    payload = verify_access_token(
        refresh_token
    )

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    if payload.get("type") != "refresh":

        raise HTTPException(
            status_code=401,
            detail="Invalid token type"
        )

    user_email = payload.get("sub")

    existing_user = db.query(User).filter(
        User.email == user_email
    ).first()

    if not existing_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if existing_user.refresh_token != refresh_token:

        raise HTTPException(
            status_code=401,
            detail="Refresh token revoked"
        )

    new_access_token = create_access_token(
        data={
            "sub": existing_user.email,
            "user_id": existing_user.id
        }
    )

    return {
        "access_token": new_access_token
    }