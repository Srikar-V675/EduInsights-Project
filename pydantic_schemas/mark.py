from datetime import datetime
from typing import Optional

from fastapi import Query
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


class MarkQueryParams:
    def __init__(
        self,
        stud_id: Optional[int] = Query(None, description="Student ID"),
        subject_id: Optional[int] = Query(None, description="Subject ID"),
        section_id: Optional[int] = Query(None, description="Section ID"),
        internal: Optional[int] = Query(None, description="Internal marks"),
        external: Optional[int] = Query(None, description="External marks"),
        total: Optional[int] = Query(None, description="Total marks"),
        result: Optional[str] = Query(None, description="Result"),
        grade: Optional[str] = Query(None, description="Grade"),
        min_total: Optional[int] = Query(None, description="Minimum total marks"),
        max_total: Optional[int] = Query(None, description="Maximum total marks"),
    ):
        self.stud_id = stud_id
        self.subject_id = subject_id
        self.section_id = section_id
        self.internal = internal
        self.external = external
        self.total = total
        self.result = result.upper() if result else None
        self.grade = grade.upper() if grade else None
        self.min_total = min_total
        self.max_total = max_total


class Mark(MarkBase):
    mark_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
