from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SectionBase(BaseModel):
    """
    Base Pydantic model for creating or updating a section.

    Attributes:
        section_name (str): The name of the section.
        semester_id (int): The ID of the semester to which the section belongs.
    """

    batch_id: int
    section: int
    num_students: int


class SectionCreate(SectionBase):
    pass


class SectionUpdate(BaseModel):
    batch_id: Optional[int]
    section: Optional[int]
    num_students: Optional[int]


class Section(SectionBase):
    section_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
