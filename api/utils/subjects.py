from typing import Sequence

from sqlalchemy import and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.subject import Subject
from pydantic_schemas.subject import SubjectCreate, SubjectQueryParams, SubjectUpdate


async def read_subjects(
    db: AsyncSession,
    query_params: SubjectQueryParams,
) -> Sequence[Subject]:
    filters = []
    if query_params.sub_code:
        filters.append(Subject.sub_code == query_params.sub_code)
    if query_params.sem_id:
        filters.append(Subject.sem_id == query_params.sem_id)
    if query_params.sub_name:
        filters.append(Subject.sub_name == query_params.sub_name)
    async with db.begin():
        query = select(Subject).where(and_(*filters))
        result = await db.execute(query)
        subjects = result.scalars().all()
        return subjects


async def read_subject(db: AsyncSession, subject_id: int) -> Subject:
    async with db.begin():
        query = select(Subject).filter(Subject.subject_id == subject_id)
        result = await db.execute(query)
        subject = result.scalar_one_or_none()
        return subject


async def add_subject(db: AsyncSession, subject: SubjectCreate) -> Subject:
    async with db.begin():
        new_subject = Subject(
            sub_code=subject.sub_code,
            sem_id=subject.sem_id,
            sub_name=subject.sub_name,
            credits=subject.credits,
        )
        db.add(new_subject)
        await db.commit()
        return new_subject


async def patch_subject(
    db: AsyncSession, subject_id: int, subject_data: SubjectUpdate
) -> Subject:
    async with db.begin():
        update_data = {}
        if subject_data.sub_code:
            update_data["sub_code"] = subject_data.sub_code
        if subject_data.sem_id:
            update_data["sem_id"] = subject_data.sem_id
        if subject_data.sub_name:
            update_data["sub_name"] = subject_data.sub_name
        if subject_data.credits:
            update_data["credits"] = subject_data.credits

        if update_data:
            query = (
                update(Subject)
                .where(Subject.subject_id == subject_id)
                .values(**update_data)
            )
            await db.execute(query)
            await db.commit()

    new_subject = await read_subject(db, subject_id)
    return new_subject


async def remove_subject(db: AsyncSession, subject_id: int) -> Subject:
    subject = await read_subject(db, subject_id)
    async with db.begin():
        await db.delete(subject)
        await db.commit()
    return subject
