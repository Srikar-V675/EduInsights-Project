import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mark import Mark
from .mixins import Timestamp
from .student import Student


class SectionName(enum.IntEnum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5


class Section(Timestamp, Base):
    """
    A class representing a section in a batch.

    Attributes:
        section_id (int): The unique identifier for the section.
        batch_id (int): The identifier of the batch to which the section belongs.
        batch (Relationship): The relationship to the Batch to which the section belongs.
        section (SectionName): The name of the section.
        num_students (int): The number of students in the section.
        marks (Relationship): The relationship to the Marks associated with the section.
        students (Relationship): The relationship to the Students in the section.
    """

    __tablename__ = "sections"

    section_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False)
    # many - one relationship -> batch
    batch = relationship("Batch", back_populates="sections")
    section = Column(Enum(SectionName), index=True, nullable=False)  # is an enum field
    num_students = Column(Integer, nullable=False)
    # avg_sgpa, ... -> add attributes as needed.

    # one-many relationship -> marks
    marks = relationship("Mark", back_populates="section")
    # one-many relationship -> students
    students = relationship("Student", back_populates="section")
