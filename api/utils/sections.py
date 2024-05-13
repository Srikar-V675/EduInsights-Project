from typing import Sequence

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.section import Section
from pydantic_schemas.section import SectionCreate, SectionUpdate


async def read_sections(db: AsyncSession) -> Sequence[Section]:
    async with db.begin():
        query = select(Section)
        result = await db.execute(query)
        sections = result.scalars().all()
        return sections


async def add_section(db: AsyncSession, section: SectionCreate) -> Section:
    async with db.begin():
        new_section = Section(
            batch_id=section.batch_id,
            section=section.section,
            num_students=section.num_students,
        )
        db.add(new_section)
        await db.commit()
        return new_section


async def read_section(db: AsyncSession, section_id: int) -> Section:
    async with db.begin():
        query = select(Section).filter(Section.section_id == section_id)
        result = await db.execute(query)
        section = result.scalar_one_or_none()
        return section


async def patch_section(
    db: AsyncSession, section_id: int, section_data: SectionUpdate
) -> Section:
    async with db.begin():
        update_data = {}
        if section_data.batch_id:
            update_data["batch_id"] = section_data.batch_id
        if section_data.section:
            update_data["section"] = section_data.section
        if section_data.num_students:
            update_data["num_students"] = section_data.num_students

        if update_data:
            query = (
                update(Section)
                .where(Section.section_id == section_id)
                .values(**update_data)
            )
            await db.execute(query)
            await db.commit()

    new_section = await read_section(db, section_id)
    return new_section


async def remove_section(db: AsyncSession, section_id: int) -> Section:
    section = await read_section(db, section_id)
    async with db.begin():
        await db.delete(section)
        await db.commit()
    return section
