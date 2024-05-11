from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Timestamp:
    """
    A mixin class to add timestamp attributes for database rows.

    Attributes:
        created_at (DateTime): The timestamp indicating when the row was created.
        updated_at (DateTime): The timestamp indicating when the row was last updated.
    """

    created_at = Column(
        DateTime, default=func.now(), nullable=False
    )  # Default value set to the current timestamp when the row is created
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )  # Default value set to the current timestamp when the row is updated
