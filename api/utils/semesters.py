from typing import Sequence

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.semester import Semester
from pydantic_schemas.semester import SemesterCreate, SemesterUpdate


async def read_semesters(db: AsyncSession) -> Sequence[Semester]:
    """
    Reads all semesters from the database.

    Args:
        db (AsyncSession): The async database session.

    Returns:
        Sequence[Semester]: A sequence of Semester objects.
    """
    async with db.begin():
        query = select(Semester)
        result = await db.execute(query)
        semesters = result.scalars().all()
        return semesters


async def add_semester(db: AsyncSession, semester: SemesterCreate) -> Semester:
    """
    Adds a new semester to the database.

    Args:
        db (AsyncSession): The async database session.
        semester (SemesterCreate): The data for the new semester.

    Returns:
        Semester: The newly created Semester object.
    """
    async with db.begin():
        new_semester = Semester(
            batch_id=semester.batch_id,
            sem_num=semester.sem_num,
            num_subjects=semester.num_subjects,
        )
        db.add(new_semester)
        await db.commit()
        return new_semester


async def patch_semester(
    db: AsyncSession, sem_id: int, semester_data: SemesterUpdate
) -> Semester:
    """
    Updates a semester in the database.

    Args:
        db (AsyncSession): The async database session.
        sem_id (int): The identifier of the semester to update.
        semester_data (SemesterUpdate): The data to update the semester with.

    Returns:
        Semester: The updated Semester object.
    """
    # semester = await read_semester(db=db, sem_id=sem_id)
    async with db.begin():
        update_data = {}
        if semester_data.batch_id:
            update_data["batch_id"] = semester_data.batch_id
        if semester_data.sem_num:
            update_data["sem_num"] = semester_data.sem_num
        if semester_data.num_subjects:
            update_data["num_subjects"] = semester_data.num_subjects

        if update_data:
            query = (
                update(Semester).where(Semester.sem_id == sem_id).values(**update_data)
            )
            await db.execute(query)
            await db.commit()
    new_semester = await read_semester(db=db, sem_id=sem_id)
    return new_semester


async def read_semester(db: AsyncSession, sem_id: int) -> Semester:
    """
    Reads a single semester from the database.

    Args:
        db (AsyncSession): The async database session.
        sem_id (int): The identifier of the semester to read.

    Returns:
        Semester: The Semester object if found, else None.
    """
    async with db.begin():
        query = select(Semester).where(Semester.sem_id == sem_id)
        result = await db.execute(query)
        semester = result.scalar_one_or_none()
        return semester


async def remove_semester(db: AsyncSession, sem_id: int) -> Semester:
    """
    Removes a semester from the database.

    Args:
        db (AsyncSession): The async database session.
        sem_id (int): The identifier of the semester to remove.

    Returns:
        Semester: The removed Semester object.
    """
    semester = await read_semester(db=db, sem_id=sem_id)
    async with db.begin():
        await db.delete(semester)
        await db.commit()
        return semester
