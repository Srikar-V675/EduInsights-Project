from typing import List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.semesters import (
    add_semester,
    patch_semester,
    read_semester,
    read_semesters,
    remove_semester,
)
from db.db_setup import get_db
from pydantic_schemas.semester import Semester, SemesterCreate, SemesterUpdate

router = fastapi.APIRouter()


@router.get("", response_model=List[Semester])
async def get_semesters(db: AsyncSession = Depends(get_db)):
    """
    Retrieves all semesters.

    Args:
        db (AsyncSession): The async database session.

    Returns:
        List[Semester]: A list of Semester objects.
    """
    semesters = await read_semesters(db)
    return semesters


@router.post("", response_model=Semester, status_code=201)
async def create_new_semester(
    semester: SemesterCreate, db: AsyncSession = Depends(get_db)
):
    """
    Creates a new semester.

    Args:
        semester (SemesterCreate): The data for the new semester.
        db (AsyncSession): The async database session.

    Returns:
        Semester: The newly created Semester object.
    """
    return await add_semester(db=db, semester=semester)


@router.get("/{sem_id}", response_model=Semester)
async def get_semester(sem_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieves a single semester by its ID.

    Args:
        sem_id (int): The ID of the semester to retrieve.
        db (AsyncSession): The async database session.

    Returns:
        Semester: The retrieved Semester object.
    """
    semester = await read_semester(db=db, sem_id=sem_id)
    if semester is None:
        raise HTTPException(status_code=404, detail="Semester not found")
    return semester


@router.patch("/{sem_id}", response_model=Semester)
async def update_semester(
    sem_id: int, semester_data: SemesterUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Updates a semester.

    Args:
        sem_id (int): The ID of the semester to update.
        semester_data (SemesterUpdate): The data to update the semester with.
        db (AsyncSession): The async database session.

    Returns:
        Semester: The updated Semester object.
    """
    semester = await read_semester(db=db, sem_id=sem_id)
    if semester is None:
        raise HTTPException(status_code=404, detail="Semester not found")
    new_semester = await patch_semester(
        db=db, sem_id=sem_id, semester_data=semester_data
    )
    return new_semester


@router.delete("/{sem_id}", response_model=Semester)
async def delete_semester(sem_id: int, db: AsyncSession = Depends(get_db)):
    """
    Deletes a semester.

    Args:
        sem_id (int): The ID of the semester to delete.
        db (AsyncSession): The async database session.

    Returns:
        Semester: The deleted Semester object.
    """
    semester = await read_semester(db=db, sem_id=sem_id)
    if semester is None:
        raise HTTPException(status_code=404, detail="Semester not found")
    await remove_semester(db=db, sem_id=sem_id)
    return semester
