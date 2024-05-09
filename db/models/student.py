from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp

# class Base(AsyncAttrs, DeclarativeBase):
#     pass


class Student(Timestamp, Base):
    __tablename__ = "students"
    __table_args__ = (
        CheckConstraint(
            "current_sem >= 1 AND current_sem <= 8",
            name="check_semester_range",
        ),
    )

    stud_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False)
    # many - one relationship -> batch
    batch = relationship("Batch", back_populates="students")
    usn = Column(String(10), unique=True, index=True, nullable=False)
    section_id = Column(
        Integer, ForeignKey("sections.section_id"), nullable=False
    )
    # many-one relationship -> section
    section = relationship("Section", back_populates="students")
    stud_name = Column(String(100), index=True, nullable=False)
    cgpa = Column(Numeric(precision=2, scale=2), default=0.0, nullable=False)
    active = Column(Boolean, index=True, default=True, nullable=False)
    current_sem = Column(Integer, index=True, default=1, nullable=False)
    # one - many relationship -> mark
    marks = relationship("Mark", back_populates="student")
