from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from datetime import datetime
from sqlalchemy import Text


from backend.database.db import Base

from sqlalchemy import Text


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        nullable=False,
        unique=True
    )

    email = Column(
        String,
        nullable=False,
        unique=True
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    is_admin = Column(
        Boolean,
        default=False
    )

    failed_login_attempts = Column(
        Integer,
        default=0
    )

    account_locked = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    refresh_token = Column(
    Text,
    nullable=True
    )
    
    two_factor_secret = Column(
    Text,
    nullable=True
    )

    two_factor_enabled = Column(
    Boolean,
    default=False
    )