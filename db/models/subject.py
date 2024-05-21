from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mark import Mark
from .mixins import Timestamp


class Subject(Timestamp, Base):
    """
    A class representing a subject taught in a semester.

    Attributes:
        subject_id (int): The unique identifier for the subject.
        sub_code (str): The code of the subject.
        sem_id (int): The identifier of the semester to which the subject belongs.
        semester (Relationship): The relationship to the Semester to which the subject belongs.
        sub_name (str): The name of the subject.
        marks (Relationship): The relationship to the Marks of the subject.
    """

    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True, index=True)
    sub_code = Column(String(10), index=True, nullable=False)
    sem_id = Column(
        Integer, ForeignKey("semesters.sem_id", ondelete="CASCADE"), nullable=False
    )
    # many - one relationship -> semester
    semester = relationship("Semester", back_populates="subjects")
    sub_name = Column(String(70), index=True, nullable=False)
    credits = Column(Integer, nullable=False)
    # avg_marks, credits, num_pass,... -> add more as needed.

    # one-many relationship -> marks
    marks = relationship("Mark", back_populates="subject", cascade="all, delete-orphan")
