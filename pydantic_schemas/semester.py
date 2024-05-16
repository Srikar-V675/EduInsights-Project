from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class SemesterBase(BaseModel):
    """
    Base Pydantic model for creating or updating a semester.

    Attributes:
        batch_id (int): The identifier of the batch associated with the semester.
        sem_num (int): The number of the semester.
        num_subjects (int): The number of subjects in the semester.
    """

    batch_id: int
    sem_num: int
    num_subjects: int


class SemesterCreate(SemesterBase):
    """
    Pydantic model for creating a new semester.

    Inherits attributes from SemesterBase.
    """

    pass


class SemesterQueryParams:
    def __init__(
        self,
        batch_id: Optional[int] = Query(None, description="Batch ID"),
        sem_num: Optional[int] = Query(None, description="Semester number"),
        num_subjects: Optional[int] = Query(None, description="Number of subjects"),
        min_subjects: Optional[int] = Query(
            None, description="Minimum number of subjects"
        ),
        max_subjects: Optional[int] = Query(
            None, description="Maximum number of subjects"
        ),
    ):
        self.batch_id = batch_id
        self.sem_num = sem_num
        self.num_subjects = num_subjects
        self.min_subjects = min_subjects
        self.max_subjects = max_subjects


class SemesterUpdate(BaseModel):
    """
    Pydantic model for updating a semester.

    Attributes:
        batch_id (Optional[int]): The updated identifier of the batch associated with the semester.
        sem_num (Optional[int]): The updated number of the semester.
        num_subjects (Optional[int]): The updated number of subjects in the semester.
    """

    batch_id: Optional[int]
    sem_num: Optional[int]
    num_subjects: Optional[int]


class Semester(SemesterBase):
    """
    Pydantic model representing a semester.

    Inherits attributes from SemesterBase and includes additional attributes for database timestamps.

    Attributes:
        sem_id (int): The unique identifier for the semester.
        created_at (datetime): The timestamp indicating when the semester was created.
        updated_at (datetime): The timestamp indicating when the semester was last updated.

    Config:
        from_attributes (bool): Indicates that the model should be constructed from database attributes.
    """

    sem_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
