from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp
from .section import Section  # Import Section model for one-to-many relationship
from .semester import Semester  # Import Semester model for one-to-many relationship
from .student import Student  # Import Student model for one-to-many relationship


class Batch(Timestamp, Base):
    """
    Represents a batch of students

    Attributes:
        batch_id (int): The unique identifier for the batch.
        dept_id (int): The ID of the department to which the batch belongs.
        department (Department): The department to which the batch belongs.
        batch_name (str): The name of the batch.
        batch_year (str): The academic year of the batch.
        scheme (int): The scheme or curriculum followed by the batch.
        num_students (int): The number of students in the batch.
        students (List[Student]): The list of students belonging to the batch.
        semesters (List[Semester]): The list of semesters associated with the batch.
        sections (List[Section]): The list of sections within the batch.
    """

    __tablename__ = "batches"
    # Check constraint to ensure start_usn is not equal to end_usn
    __table_args__ = (
        CheckConstraint("start_usn != end_usn", name="start_usn_not_equal_end_usn"),
    )

    batch_id = Column(Integer, primary_key=True, index=True)
    dept_id = Column(Integer, ForeignKey("departments.dept_id"), nullable=False)
    department = relationship(
        "Department", back_populates="batches"
    )  # many-to-one relationship with Department
    batch_name = Column(String(50), unique=True, index=True, nullable=False)
    batch_start_year = Column(Integer, index=True, nullable=False)
    batch_end_year = Column(Integer, index=True, nullable=False)
    scheme = Column(Integer, index=True, nullable=False)
    start_usn = Column(String(10), nullable=False)
    end_usn = Column(String(10), nullable=False)
    lateral_start_usn = Column(String(10), nullable=True)
    lateral_end_usn = Column(String(10), nullable=True)
    num_students = Column(Integer, default=0, nullable=False)

    # Define one-to-many relationships with Student, Semester, and Section models
    students = relationship(
        "Student", back_populates="batch"
    )  # one-to-many relationship with Student
    semesters = relationship(
        "Semester", back_populates="batch"
    )  # one-to-many relationship with Semester
    sections = relationship(
        "Section", back_populates="batch"
    )  # one-to-many relationship with Section
