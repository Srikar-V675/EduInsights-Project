from typing import Sequence

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.mark import Mark
from pydantic_schemas.mark import MarkCreate, MarkUpdate


async def read_marks(db: AsyncSession) -> Sequence[Mark]:
    async with db.begin():
        query = select(Mark)
        result = await db.execute(query)
        marks = result.scalars().all()
        return marks


async def add_mark(db: AsyncSession, mark: MarkCreate) -> Mark:
    async with db.begin():
        new_mark = Mark(
            stud_id=mark.stud_id,
            subject_id=mark.subject_id,
            section_id=mark.section_id,
            internal=mark.internal,
            external=mark.external,
            total=mark.total,
            result=mark.result,
            grade=mark.grade,
        )
        db.add(new_mark)
        await db.commit()
        return new_mark


async def read_mark(db: AsyncSession, mark_id: int) -> Mark:
    async with db.begin():
        query = select(Mark).filter(Mark.mark_id == mark_id)
        result = await db.execute(query)
        mark = result.scalar_one_or_none()
        return mark


async def patch_mark(db: AsyncSession, mark_id: int, mark_data: MarkUpdate) -> Mark:
    async with db.begin():
        update_data = {}
        if mark_data.stud_id:
            update_data["stud_id"] = mark_data.stud_id
        if mark_data.subject_id:
            update_data["subject_id"] = mark_data.subject_id
        if mark_data.section_id:
            update_data["section_id"] = mark_data.section_id
        if mark_data.internal:
            update_data["internal"] = mark_data.internal
        if mark_data.external:
            update_data["external"] = mark_data.external
        if mark_data.total:
            update_data["total"] = mark_data.total
        if mark_data.result:
            update_data["result"] = mark_data.result
        if mark_data.grade:
            update_data["grade"] = mark_data.grade

        if update_data:
            query = update(Mark).where(Mark.mark_id == mark_id).values(**update_data)
            await db.execute(query)
            await db.commit()

    new_mark = await read_mark(db, mark_id)
    return new_mark


async def remove_mark(db: AsyncSession, mark_id: int) -> Mark:
    mark = await read_mark(db, mark_id)
    async with db.begin():
        await db.delete(mark)
        await db.commit()
    return mark
