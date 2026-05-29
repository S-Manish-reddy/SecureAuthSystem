from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from backend.database.db import get_db

from backend.models.security_event_model import SecurityEvent

router = APIRouter()


@router.get("/security-events")
def get_security_events(
    db: Session = Depends(get_db)
):

    events = db.query(SecurityEvent).all()

    return events


@router.get("/security-stats")
def get_security_stats(
    db: Session = Depends(get_db)
):

    total_events = db.query(SecurityEvent).count()

    failed_logins = db.query(SecurityEvent).filter(
        SecurityEvent.event_type == "FAILED_LOGIN"
    ).count()

    locked_accounts = db.query(SecurityEvent).filter(
        SecurityEvent.event_type == "ACCOUNT_LOCKED"
    ).count()

    successful_logins = db.query(SecurityEvent).filter(
        SecurityEvent.event_type == "SUCCESSFUL_LOGIN"
    ).count()

    return {
        "total_security_events": total_events,
        "failed_logins": failed_logins,
        "locked_accounts": locked_accounts,
        "successful_logins": successful_logins
    }