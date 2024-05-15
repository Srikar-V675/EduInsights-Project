from datetime import datetime
from typing import Optional

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


class Section(SectionBase):
    section_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
