from backend.models.security_event_model import SecurityEvent


def log_security_event(
    db,
    event_type,
    user_email,
    ip_address,
    description
):

    event = SecurityEvent(
        event_type=event_type,
        user_email=user_email,
        ip_address=ip_address,
        description=description
    )

    db.add(event)

    db.commit()