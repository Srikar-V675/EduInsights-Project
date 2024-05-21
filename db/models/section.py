from sqlalchemy import CheckConstraint, Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import String

from ..db_setup import Base
from .extraction import Extraction
from .mark import Mark
from .mixins import Timestamp
from .student import Student


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
    # Check constraint to ensure start_usn is not equal to end_usn
    __table_args__ = (
        CheckConstraint("start_usn != end_usn", name="start_usn_not_equal_end_usn"),
    )

    section_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(
        Integer, ForeignKey("batches.batch_id", ondelete="CASCADE"), nullable=False
    )
    # many - one relationship -> batch
    batch = relationship("Batch", back_populates="sections")
    section = Column(String(1), index=True, nullable=False)  # is an enum field
    start_usn = Column(String(10), nullable=False)
    end_usn = Column(String(10), nullable=False)
    lateral_start_usn = Column(String(10), nullable=True)
    lateral_end_usn = Column(String(10), nullable=True)
    num_students = Column(Integer, default=0, nullable=False)
    # avg_sgpa, ... -> add attributes as needed.

    # one-many relationship -> marks
    marks = relationship("Mark", back_populates="section", cascade="all, delete-orphan")
    # one-many relationship -> students
    students = relationship(
        "Student", back_populates="section", cascade="all, delete-orphan"
    )
    # one-many relationship -> extractions
    extractions = relationship(
        "Extraction", back_populates="section", cascade="all, delete-orphan"
    )
