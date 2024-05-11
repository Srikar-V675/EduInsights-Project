import enum

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Enum

from ..db_setup import Base
from .batch import Batch  # Import Batch model for one-to-many relationship
from .mixins import Timestamp


class Depts(enum.IntEnum):
    """
    Enumeration representing various departments.

    Attributes:
        CSE (int): Computer Science and Engineering department.
        ISE (int): Information Science and Engineering department.
        AIML (int): Artificial Intelligence and Machine Learning department.
        ECE (int): Electronics and Communication Engineering department.
        EEE (int): Electrical and Electronics Engineering department.
        MECH (int): Mechanical Engineering department.
        CIVIL (int): Civil Engineering department.
    """

    CSE = 1
    ISE = 2
    AIML = 3
    ECE = 4
    EEE = 5
    MECH = 6
    CIVIL = 7


class Department(Timestamp, Base):
    """
    Represents a department.

    Attributes:
        dept_id (int): The unique identifier for the department.
        dept_name (Depts): The name of the department.
        password (str): The password for the department.
        batches (List[Batch]): The list of batches associated with the department.
    """

    __tablename__ = "departments"

    dept_id = Column(Integer, primary_key=True, index=True)
    dept_name = Column(Enum(Depts), index=True, nullable=False)
    password = Column(Text, nullable=False)

    # Define one-to-many relationship with Batch model
    batches = relationship(
        "Batch", back_populates="department"
    )  # one-to-many relationship with Batch
