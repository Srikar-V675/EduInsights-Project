from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, HttpUrl, validator


class IdentifySubjects(BaseModel):
    # add type -> PDF or Scraper
    usn: Optional[str] = None
    result_url: HttpUrl

    @validator("usn")
    def usn_must_be_valid(cls, v):
        if v != "":
            if len(v) != 10:
                raise ValueError("USN must be 10 characters long")
        if v is None or v == "":
            return None
        return v


class SubjectSchema(BaseModel):
    sub_code: str
    sub_name: str
    credits: int


class ExtractBody(BaseModel):
    section_id: int
    result_url: HttpUrl
    # add type -> PDF or Scraper


class ExtractResponse(BaseModel):
    message: str
    extraction_id: int


class ExtractionBase(BaseModel):
    section_id: int
    sem_id: int
    total_usns: int
    num_completed: int
    num_invalid: int
    reattempts: int
    progress: float
    completed: bool
    failed: bool
    time_taken: float


class ExtractionCreate(ExtractionBase):
    pass


class ExtractionUpdate(BaseModel):
    section_id: Optional[int] = None
    sem_id: Optional[int] = None
    total_usns: Optional[int] = None
    num_completed: Optional[int] = None
    num_invalid: Optional[int] = None
    reattempts: Optional[int] = None
    progress: Optional[float] = None
    completed: Optional[bool] = None
    failed: Optional[bool] = None
    time_taken: Optional[float] = None


class ExtractionQueryParams:
    def __init__(
        self,
        section_id: Optional[int] = Query(None, description="Section ID"),
        sem_id: Optional[int] = Query(None, description="Semester ID"),
        total_usns: Optional[int] = Query(None, description="Total USNs"),
        num_completed: Optional[int] = Query(
            None, description="Number of USNs completed"
        ),
        num_invalid: Optional[int] = Query(None, description="Number of invalid USNs"),
        reattempts: Optional[int] = Query(None, description="Number of reattempts"),
        progress: Optional[float] = Query(None, description="Progress"),
        completed: Optional[bool] = Query(None, description="Extraction completed"),
        failed: Optional[bool] = Query(None, description="Extraction failed"),
        time_taken: Optional[float] = Query(
            None, description="Time taken for extraction"
        ),
    ):
        self.section_id = section_id
        self.sem_id = sem_id
        self.total_usns = total_usns
        self.num_completed = num_completed
        self.num_invalid = num_invalid
        self.reattempts = reattempts
        self.progress = progress
        self.completed = completed
        self.failed = failed
        self.time_taken = time_taken


class Extraction(ExtractionBase):
    extraction_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
