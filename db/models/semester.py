from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp

# class Base(AsyncAttrs, DeclarativeBase):
#     pass


class Semester(Timestamp, Base):
    __tablename__ = "semesters"
    __table_args__ = (
        CheckConstraint(
            "sem_num >= 1 AND sem_num <= 8", name="check_semester_range"
        ),
    )

    sem_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False)
    # many - one relationship -> batch
    batch = relationship("Batch", back_populates="semesters")
    sem_num = Column(Integer, index=True, nullable=False, default=1)
    num_subjects = Column(Integer, index=True, nullable=False)

    # one - many relationship -> sections
    sections = relationship("Section", back_populates="semester")
    # one-many relationship -> subjects
    subjects = relationship("Subject", back_populates="semester")
    # one-many relationship -> marks
    marks = relationship("Mark", back_populates="semester")
