from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp

# class Base(AsyncAttrs, DeclarativeBase):
#     pass


class Batch(Timestamp, Base):
    __tablename__ = "batches"

    batch_id = Column(Integer, primary_key=True, index=True)
    batch_name = Column(String(50), unique=True, index=True, nullable=False)
    batch_year = Column(String(9), index=True, nullable=False)
    scheme = Column(Integer, index=True, nullable=False)
    num_students = Column(Integer, default=0, nullable=False)

    # one to many relationship -> students
    students = relationship("Student", back_populates="batch")
    # one - many relationship -> semesters
    semesters = relationship("Semester", back_populates="batch")
    # one - many relationship -> sections
    sections = relationship("Section", back_populates="batch")
    # one-many relationship -> subjects
    subjects = relationship("Subject", back_populates="batch")
    # one-many relationship -> marks
    marks = relationship("Mark", back_populates="batch")
