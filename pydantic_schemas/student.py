from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class StudentBase(BaseModel):
    batch_id: int
    usn: str
    section_id: int
    stud_name: str
    cgpa: float
    active: bool
    current_sem: int


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    batch_id: Optional[int] = None
    usn: Optional[str] = None
    section_id: Optional[int] = None
    stud_name: Optional[str] = None
    cgpa: Optional[float] = None
    active: Optional[bool] = None
    current_sem: Optional[int] = None


class StudentQueryParams:
    def __init__(
        self,
        batch_id: Optional[int] = Query(None, description="Batch ID"),
        usn: Optional[str] = Query(None, description="USN"),
        section_id: Optional[int] = Query(None, description="Section ID"),
        stud_name: Optional[str] = Query(None, description="Student name"),
        cgpa: Optional[float] = Query(None, description="CGPA"),
        min_cgpa: Optional[float] = Query(None, description="Minimum CGPA"),
        max_cgpa: Optional[float] = Query(None, description="Maximum CGPA"),
        active: Optional[bool] = Query(None, description="Active status"),
        current_sem: Optional[int] = Query(None, description="Current Semester"),
    ):
        self.batch_id = batch_id
        self.usn = usn.upper() if usn else None
        self.section_id = section_id
        self.stud_name = stud_name
        self.cgpa = cgpa
        self.min_cgpa = min_cgpa
        self.max_cgpa = max_cgpa
        self.active = active
        self.current_sem = current_sem


class Student(StudentBase):
    stud_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
