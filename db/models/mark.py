import enum

from sqlalchemy import CheckConstraint, Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp

# class Base(AsyncAttrs, DeclarativeBase):
#     pass


class Results(enum.IntEnum):
    F = 0
    P = 1
    W = 2


class Grades(enum.IntEnum):
    FCD = 1
    FC = 2
    SC = 3
    FAIL = 4
    ABSENT = 5


class Mark(Timestamp, Base):
    __tablename__ = "marks"
    __table_args__ = (
        CheckConstraint("internal <= 50", name="check_internal"),
        CheckConstraint("external <= 50", name="check_external"),
        CheckConstraint("total <= 100", name="check_total"),
    )

    marks_id = Column(Integer, primary_key=True, index=True)
    stud_id = Column(Integer, ForeignKey("students.stud_id"), nullable=False)
    # many-one relationship -> student
    student = relationship("Student", back_populates="marks")
    subject_id = Column(
        Integer, ForeignKey("subjects.subject_id"), nullable=False
    )
    # many-one relationship -> subject
    subject = relationship("Subject", back_populates="marks")
    section_id = Column(
        Integer, ForeignKey("sections.section_id"), nullable=False
    )
    # many-one relationship -> section
    section = relationship("Section", back_populates="marks")
    sem_id = Column(Integer, ForeignKey("semesters.sem_id"), nullable=False)
    # many-one relationship -> semester
    semester = relationship("Semester", back_populates="marks")
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False)
    # many-one relationship -> batch
    batch = relationship("Batch", back_populates="marks")
    internal = Column(Integer, index=True, nullable=False)
    external = Column(Integer, index=True, nullable=False)
    total = Column(Integer, index=True, nullable=False)
    result = Column(Enum(Results), nullable=False)
    grade = Column(Enum(Grades), nullable=False)
