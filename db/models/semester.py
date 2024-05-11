from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp
from .subject import Subject


class Semester(Timestamp, Base):
    """
    A class representing a semester in a batch.

    Attributes:
        sem_id (int): The unique identifier for the semester.
        batch_id (int): The identifier of the batch to which the semester belongs.
        batch (Relationship): The relationship to the Batch to which the semester belongs.
        sem_num (int): The semester number.
        num_subjects (int): The number of subjects in the semester.
        subjects (Relationship): The relationship to the Subjects in the semester.
    """

    __tablename__ = "semesters"
    __table_args__ = (
        CheckConstraint("sem_num >= 1 AND sem_num <= 8", name="check_semester_range"),
    )

    sem_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False)
    # many - one relationship -> batch
    batch = relationship("Batch", back_populates="semesters")
    sem_num = Column(Integer, index=True, nullable=False, default=1)
    num_subjects = Column(Integer, index=True, nullable=False)

    # one-many relationship -> subjects
    subjects = relationship("Subject", back_populates="semester")
