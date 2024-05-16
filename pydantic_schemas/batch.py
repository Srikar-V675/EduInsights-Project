from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class BatchBase(BaseModel):
    """
    Base Pydantic model for creating or updating a batch.

    Attributes:
        dept_id (int): The department ID to which the batch belongs.
        batch_name (str): The name of the batch.
        batch_year (str): The year of the batch.
        scheme (int): The scheme of the batch.
        num_students (int): The number of students in the batch.
    """

    dept_id: int
    batch_name: str
    batch_start_year: int
    batch_end_year: int
    scheme: int
    num_students: int


class BatchCreate(BatchBase):
    """
    Pydantic model for creating a new batch.

    Inherits attributes from BatchBase.
    """

    pass


class BatchUpdate(BaseModel):
    dept_id: Optional[int]
    batch_name: Optional[str]
    batch_start_year: Optional[int]
    batch_end_year: Optional[int]
    scheme: Optional[int]
    num_students: Optional[int]


class BatchQueryParams:
    def __init__(
        self,
        dept_id: Optional[int] = Query(None, description="Department ID"),
        batch_name: Optional[str] = Query(None, description="Batch name"),
        batch_start_year: Optional[int] = Query(
            None, description="Start year of the batch"
        ),
        batch_end_year: Optional[int] = Query(
            None, description="End year of the batch"
        ),
        scheme: Optional[int] = Query(None, description="Scheme of the batch"),
        min_students: Optional[int] = Query(
            None, description="Minimum number of students"
        ),
        max_students: Optional[int] = Query(
            None, description="Maximum number of students"
        ),
    ):
        self.dept_id = dept_id
        self.batch_name = batch_name
        self.batch_start_year = batch_start_year
        self.batch_end_year = batch_end_year
        self.scheme = scheme
        self.min_students = min_students
        self.max_students = max_students


class Batch(BatchBase):
    """
    Pydantic model representing a batch.

    Inherits attributes from BatchBase and includes additional attributes for database timestamps.

    Attributes:
        batch_id (int): The unique identifier for the batch.
        created_at (datetime): The timestamp indicating when the batch was created.
        updated_at (datetime): The timestamp indicating when the batch was last updated.

    Config:
        from_attributes (bool): Indicates that the model should be constructed from database attributes.
    """

    batch_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
