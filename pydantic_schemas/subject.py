from datetime import datetime
from typing import Optional

from fastapi import Query
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


class SubjectQueryParams:
    def __init__(
        self,
        sub_code: Optional[str] = Query(None, description="Subject code"),
        sem_id: Optional[int] = Query(None, description="Semester ID"),
        sub_name: Optional[str] = Query(None, description="Subject name"),
    ):
        self.sub_code = sub_code.upper() if sub_code else None
        self.sem_id = sem_id
        self.sub_name = sub_name


class Subject(SubjectBase):
    subject_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
