from typing import List

import fastapi
from fastapi import BackgroundTasks, Depends, HTTPException
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from api.utils.extractions.scraper import scrape_section
from api.utils.extractions.subjects import add_subjects, identify_subjects
from db.db_setup import get_db, get_session_factory
from pydantic_schemas.extraction import IdentifySubjects, SubjectSchema

router = fastapi.APIRouter()


@router.post("/identify_subjects/{batch_id}", response_model=List[SubjectSchema])
async def extract_subjects(
    batch_id: int,
    data: IdentifySubjects,
    db: AsyncSession = Depends(get_db),
):
    try:
        subjects = await identify_subjects(batch_id, data, db)
        return subjects
    except HTTPException as e:
        raise HTTPException(status_code=422, detail=e.detail)


@router.post("/add_subjects/{batch_id}", response_model=List[SubjectSchema])
async def create_subjects_after_extracting(
    batch_id: int,
    subjects: List[SubjectSchema],
    db: AsyncSession = Depends(get_db),
):
    try:
        subjects = await add_subjects(batch_id, subjects, db)
        return subjects
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/scraper/{section_id}")
async def scrape_section_results(
    section_id: int,
    result_url: HttpUrl,
    background_tasks: BackgroundTasks,
    session_factory: sessionmaker = Depends(get_session_factory),
):
    try:
        message = await scrape_section(
            section_id, result_url, background_tasks, session_factory
        )
        return message
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
