from datetime import datetime
from typing import Optional

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
    batch_id: Optional[int]
    usn: Optional[str]
    section_id: Optional[int]
    stud_name: Optional[str]
    cgpa: Optional[float]
    active: Optional[bool]
    current_sem: Optional[int]


class Student(StudentBase):
    stud_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
