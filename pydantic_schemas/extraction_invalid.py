from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExtractionInvalidBase(BaseModel):
    extraction_id: int
    invalid_usns: str
    captcha_usns: str
    timeout_usns: str


class ExtractionInvalidCreate(ExtractionInvalidBase):
    pass


class ExtractionInvalidUpdate(BaseModel):
    extraction_id: Optional[int] = None
    invalid_usns: Optional[str] = None
    captcha_usns: Optional[str] = None
    timeout_usns: Optional[str] = None


class ExtractionInvalid(ExtractionInvalidBase):
    invalid_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
