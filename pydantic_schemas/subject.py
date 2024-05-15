from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SubjectBase(BaseModel):
    sub_code: str
    sem_id: int
    sub_name: str


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    sub_code: Optional[str]
    sem_id: Optional[int]
    sub_name: Optional[str]


class Subject(SubjectBase):
    subject_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
