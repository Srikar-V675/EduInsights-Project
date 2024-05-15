from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class MarkBase(BaseModel):
    stud_id: int
    subject_id: int
    section_id: int
    internal: int
    external: int
    total: int
    result: str
    grade: str

    @validator("result")
    def validate_result(cls, v):
        if v not in ["F", "P", "W"]:
            raise ValueError("Invalid result")
        return v

    @validator("grade")
    def validate_grade(cls, v):
        if v not in ["FCD", "FC", "SC", "FAIL", "ABSENT"]:
            raise ValueError("Invalid grade")
        return v


class MarkCreate(MarkBase):
    pass


class MarkUpdate(BaseModel):
    stud_id: Optional[int]
    subject_id: Optional[int]
    section_id: Optional[int]
    internal: Optional[int]
    external: Optional[int]
    total: Optional[int]
    result: Optional[str]
    grade: Optional[str]

    @validator("result", pre=True, always=True)
    def validate_result(cls, v):
        if v is None or v not in ["F", "P", "W"]:
            return "W"
        return v

    @validator("grade", pre=True, always=True)
    def validate_grade(cls, v):
        if v is None or v not in ["FCD", "FC", "SC", "FAIL", "ABSENT"]:
            return "ABSENT"
        return v


class Mark(MarkBase):
    mark_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
