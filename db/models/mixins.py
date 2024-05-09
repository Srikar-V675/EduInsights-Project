from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin


@declarative_mixin  # mixins are used here for having timestamp of created and updated for the rows in db
class Timestamp:
    created_at = Column(
        DateTime, default=datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )
