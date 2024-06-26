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
from .mark import Mark
from .mixins import Timestamp
from .student_performance import StudentPerformance


class Student(Timestamp, Base):
    """
    A class representing a student in a batch.

    Attributes:
        stud_id (int): The unique identifier for the student.
        batch_id (int): The identifier of the batch to which the student belongs.
        batch (Relationship): The relationship to the Batch to which the student belongs.
        usn (str): The unique student number.
        section_id (int): The identifier of the section to which the student belongs.
        section (Relationship): The relationship to the Section to which the student belongs.
        stud_name (str): The name of the student.
        cgpa (float): The cumulative grade point average of the student.
        active (bool): A flag indicating whether the student is active or not.
        current_sem (int): The current semester of the student.
        marks (Relationship): The relationship to the Marks of the student.
    """

    __tablename__ = "students"

    stud_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(
        Integer, ForeignKey("batches.batch_id", ondelete="CASCADE"), nullable=False
    )
    # many - one relationship -> batch
    batch = relationship("Batch", back_populates="students")
    usn = Column(String(10), unique=True, index=True, nullable=False)
    section_id = Column(
        Integer, ForeignKey("sections.section_id", ondelete="CASCADE"), nullable=False
    )
    # many-one relationship -> section
    section = relationship("Section", back_populates="students")
    stud_name = Column(String(100), index=True, nullable=False)
    cgpa = Column(Numeric(precision=3, scale=1), default=0.0, nullable=False)
    active = Column(Boolean, index=True, default=True, nullable=False)
    current_sem = Column(
        Integer, ForeignKey("semesters.sem_id", ondelete="CASCADE"), nullable=False
    )
    # many-one relationship -> semester
    semester = relationship("Semester", back_populates="students")
    # one - many relationship -> mark
    marks = relationship("Mark", back_populates="student", cascade="all, delete-orphan")
    # one - many relationship -> student_performance
    student_performances = relationship(
        "StudentPerformance", back_populates="student", cascade="all, delete-orphan"
    )
