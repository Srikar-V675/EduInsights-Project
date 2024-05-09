import enum

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp

# class Base(AsyncAttrs, DeclarativeBase):
#     pass


class Sections(enum.IntEnum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5


class Section(Timestamp, Base):
    __tablename__ = "sections"

    section_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False)
    # many - one relationship -> batch
    batch = relationship("Batch", back_populates="sections")
    sem_id = Column(Integer, ForeignKey("semesters.sem_id"), nullable=False)
    # many - one relationship -> semester
    semester = relationship("Semester", back_populates="sections")
    section = Column(
        String(2), index=True, nullable=False
    )  # not enum but it is a combination of semester and section -> 3A, 5C...
    num_students = Column(Integer, nullable=False)
    # avg_sgpa, ... -> add attributes as needed.

    # one-many relationship -> marks
    marks = relationship("Mark", back_populates="section")
    # one-many relationship -> students
    students = relationship("Student", back_populates="section")
