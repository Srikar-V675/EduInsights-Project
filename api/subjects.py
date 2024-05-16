from typing import List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.subjects import (
    add_subject,
    patch_subject,
    read_subject,
    read_subjects,
    remove_subject,
)
from db.db_setup import get_db
from pydantic_schemas.subject import (
    Subject,
    SubjectCreate,
    SubjectQueryParams,
    SubjectUpdate,
)

router = fastapi.APIRouter()


# Route to retrieve all subjects
@router.get("", response_model=List[Subject])
async def get_subjects(
    query_params: SubjectQueryParams = Depends(), db: AsyncSession = Depends(get_db)
):
    subjects = await read_subjects(db, query_params)
    return subjects


# Route to create a new subject
@router.post("", response_model=Subject, status_code=201)
async def create_new_subject(
    subject: SubjectCreate, db: AsyncSession = Depends(get_db)
):
    subject = await add_subject(db=db, subject=subject)
    return subject


# Route to retrieve a specific subject by its ID
@router.get("/{subject_id}", response_model=Subject)
async def get_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    subject = await read_subject(db, subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


# Route to update a specific subject by its ID
@router.patch("/{subject_id}", response_model=Subject)
async def update_subject(
    subject_id: int, subject_data: SubjectUpdate, db: AsyncSession = Depends(get_db)
):
    subject = await read_subject(db, subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    new_subject = await patch_subject(db, subject_id, subject_data)
    return new_subject


# Route to delete a specific subject by its ID
@router.delete("/{subject_id}", response_model=Subject)
async def delete_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    subject = await read_subject(db, subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    subject = await remove_subject(db, subject_id)
    return subject
