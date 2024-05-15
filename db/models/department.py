import enum

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Enum

from ..db_setup import Base
from .batch import Batch  # Import Batch model for one-to-many relationship
from .mixins import Timestamp


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
    dept_name = Column(String, index=True, nullable=False)
    password = Column(Text, nullable=False)

    # Define one-to-many relationship with Batch model
    batches = relationship(
        "Batch", back_populates="department"
    )  # one-to-many relationship with Batch
