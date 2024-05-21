from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, validator


class StudentPerformanceBase(BaseModel):
    stud_id: int
    sem_id: int
    total: int
    percentage: float
    sgpa: float

    @validator("percentage")
    def validate_percentage(cls, v):
        if v < 0 or v > 100:
            raise ValueError("Invalid percentage")
        return v

    @validator("sgpa")
    def validate_sgpa(cls, v):
        if v < 0 or v > 10:
            raise ValueError("Invalid sgpa")
        return v


class StudentPerformanceCreate(StudentPerformanceBase):
    pass


class StudentPerformanceUpdate(BaseModel):
    stud_id: Optional[int]
    sem_id: Optional[int]
    total: Optional[int]
    percentage: Optional[float]
    sgpa: Optional[float]

    @validator("percentage", pre=True, always=True)
    def validate_percentage(cls, v):
        if v is None:
            return 0.0
        if v < 0 or v > 100:
            return 0.0
        return v

    @validator("sgpa", pre=True, always=True)
    def validate_sgpa(cls, v):
        if v is None:
            return 0.0
        if v < 0 or v > 10:
            return 0.0
        return v


class StudentPerformanceQueryParams:
    def __init__(
        self,
        stud_perf_id: Optional[int] = Query(None, description="Student Performance ID"),
        stud_id: Optional[int] = Query(None, description="Student ID"),
        sem_id: Optional[int] = Query(None, description="Semester ID"),
        total: Optional[int] = Query(None, description="Total marks"),
        percentage: Optional[float] = Query(None, description="Percentage"),
        sgpa: Optional[float] = Query(None, description="SGPA"),
        min_total: Optional[int] = Query(None, description="Minimum total marks"),
        max_total: Optional[int] = Query(None, description="Maximum total marks"),
        min_percentage: Optional[float] = Query(None, description="Minimum percentage"),
        max_percentage: Optional[float] = Query(None, description="Maximum percentage"),
        min_sgpa: Optional[float] = Query(None, description="Minimum sgpa"),
        max_sgpa: Optional[float] = Query(None, description="Maximum sgpa"),
    ):
        self.stud_perf_id = stud_perf_id
        self.stud_id = stud_id
        self.sem_id = sem_id
        self.total = total
        self.percentage = percentage
        self.sgpa = sgpa
        self.min_total = min_total
        self.max_total = max_total
        self.min_percentage = min_percentage
        self.max_percentage = max_percentage
        self.min_sgpa = min_sgpa
        self.max_sgpa = max_sgpa


class StudentPerformance(StudentPerformanceBase):
    stud_perf_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
