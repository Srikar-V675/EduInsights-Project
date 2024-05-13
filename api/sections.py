from typing import List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.sections import (
    add_section,
    patch_section,
    read_section,
    read_sections,
    remove_section,
)
from db.db_setup import get_db
from pydantic_schemas.section import Section, SectionCreate, SectionUpdate

router = fastapi.APIRouter()


@router.get("", response_model=List[Section])
async def get_sections(db: AsyncSession = Depends(get_db)):
    sections = await read_sections(db)
    return sections


@router.post("", response_model=Section, status_code=201)
async def create_new_section(
    section: SectionCreate, db: AsyncSession = Depends(get_db)
):
    section = await add_section(db=db, section=section)
    return section


@router.get("/{section_id}", response_model=Section)
async def get_section(section_id: int, db: AsyncSession = Depends(get_db)):
    section = await read_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return section


@router.patch("/{section_id}", response_model=Section)
async def update_section(
    section_id: int, section_data: SectionUpdate, db: AsyncSession = Depends(get_db)
):
    section = await read_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    new_section = await patch_section(db, section_id, section_data)
    return new_section


@router.delete("/{section_id}", response_model=Section)
async def delete_section(section_id: int, db: AsyncSession = Depends(get_db)):
    section = await read_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    section = await remove_section(db, section_id)
    return section
