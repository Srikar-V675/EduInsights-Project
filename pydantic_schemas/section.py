from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, validator


class SectionBase(BaseModel):
    """
    Base Pydantic model for creating or updating a section.

    Attributes:
        section_name (str): The name of the section.
        semester_id (int): The ID of the semester to which the section belongs.
    """

    batch_id: int
    section: str
    num_students: int

    @validator("section")
    def validate_section(cls, v):
        if not v.isalpha() or len(v) > 1 or not v.isupper():
            raise ValueError("Section name must be a single alphabet character.")
        return v


class SectionCreate(SectionBase):
    pass


class SectionUpdate(BaseModel):
    batch_id: Optional[int]
    section: Optional[str]
    num_students: Optional[int]

    @validator("section", pre=True, always=True)
    def validate_section(cls, v):
        if v and (not v.isalpha() or len(v) > 1 or not v.isupper()):
            raise ValueError("Section name must be a single alphabet character.")
        return v


class SectionQueryParams:
    def __init__(
        self,
        batch_id: Optional[int] = Query(None, description="Batch ID"),
        section: Optional[str] = Query(None, description="Section name"),
        num_students: Optional[int] = Query(None, description="Number of students"),
        min_students: Optional[int] = Query(
            None, description="Minimum number of students"
        ),
        max_students: Optional[int] = Query(
            None, description="Maximum number of students"
        ),
    ):
        self.batch_id = batch_id
        self.section = section
        self.num_students = num_students
        self.min_students = min_students
        self.max_students = max_students


class Section(SectionBase):
    section_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
