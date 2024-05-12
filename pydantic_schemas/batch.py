from datetime import datetime
from typing import Optional

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
    batch_year: str
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
    batch_year: Optional[str]
    scheme: Optional[int]
    num_students: Optional[int]


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
