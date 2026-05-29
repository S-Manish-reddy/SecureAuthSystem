from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from backend.database.db import Base


class SecurityEvent(Base):

    __tablename__ = "security_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    event_type = Column(
        String,
        nullable=False
    )

    user_email = Column(
        String,
        nullable=True
    )

    ip_address = Column(
        String,
        nullable=True
    )

    description = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )