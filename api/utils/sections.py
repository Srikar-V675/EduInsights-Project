from typing import Sequence

from sqlalchemy import and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.section import Section
from pydantic_schemas.section import SectionCreate, SectionQueryParams, SectionUpdate


async def read_sections(
    db: AsyncSession,
    query_params: SectionQueryParams,
) -> Sequence[Section]:
    filters = []
    if query_params.batch_id:
        filters.append(Section.batch_id == query_params.batch_id)
    if query_params.section:
        filters.append(Section.section == query_params.section)
    if query_params.num_students:
        filters.append(Section.num_students == query_params.num_students)
    if query_params.min_students:
        filters.append(Section.num_students >= query_params.min_students)
    if query_params.max_students:
        filters.append(Section.num_students <= query_params.max_students)
    async with db.begin():
        query = select(Section).where(and_(*filters))
        result = await db.execute(query)
        sections = result.scalars().all()
        return sections


async def add_section(db: AsyncSession, section: SectionCreate) -> Section:
    async with db.begin():
        new_section = Section(
            batch_id=section.batch_id,
            section=section.section,
            start_usn=section.start_usn,
            end_usn=section.end_usn,
            lateral_start_usn=section.lateral_start_usn,
            lateral_end_usn=section.lateral_end_usn,
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
        if section_data.start_usn:
            update_data["start_usn"] = section_data.start_usn
        if section_data.end_usn:
            update_data["end_usn"] = section_data.end_usn
        if section_data.lateral_start_usn:
            update_data["lateral_start_usn"] = section_data.lateral_start_usn
        if section_data.lateral_end_usn:
            update_data["lateral_end_usn"] = section_data.lateral_end_usn

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
