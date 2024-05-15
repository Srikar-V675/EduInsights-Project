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


# Route to retrieve all sections
@router.get("", response_model=List[Section])
async def get_sections(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all sections.

    Args:
        db (AsyncSession): An asynchronous database session.

    Returns:
        List[Section]: A list of Section objects representing all sections in the database.
    """
    sections = await read_sections(db)
    return sections


# Route to create a new section
@router.post("", response_model=Section, status_code=201)
async def create_new_section(
    section: SectionCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new section.

    Args:
        section (SectionCreate): Data for the new section.
        db (AsyncSession): An asynchronous database session.

    Returns:
        Section: The newly created section.

    Note: Allowed section names are single uppercase alphabet characters.
    """
    section = await add_section(db=db, section=section)
    return section


# Route to retrieve a specific section by its ID
@router.get("/{section_id}", response_model=Section)
async def get_section(section_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific section by its ID.

    Args:
        section_id (int): The ID of the section to retrieve.
        db (AsyncSession): An asynchronous database session.

    Returns:
        Section: The retrieved section.

    Raises:
        HTTPException: If the section with the specified ID is not found.
    """
    section = await read_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return section


# Route to update a specific section by its ID
@router.patch("/{section_id}", response_model=Section)
async def update_section(
    section_id: int, section_data: SectionUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Update a specific section by its ID.

    Args:
        section_id (int): The ID of the section to update.
        section_data (SectionUpdate): Data containing the fields to be updated for the section.
        db (AsyncSession): An asynchronous database session.

    Returns:
        Section: The updated section.

    Raises:
        HTTPException: If the section with the specified ID is not found.

    Note: Allowed section names are single uppercase alphabet characters.
    """
    section = await read_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    new_section = await patch_section(db, section_id, section_data)
    return new_section


# Route to delete a specific section by its ID
@router.delete("/{section_id}", response_model=Section)
async def delete_section(section_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a specific section by its ID.

    Args:
        section_id (int): The ID of the section to delete.
        db (AsyncSession): An asynchronous database session.

    Returns:
        Section: The deleted section.

    Raises:
        HTTPException: If the section with the specified ID is not found.
    """
    section = await read_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    section = await remove_section(db, section_id)
    return section
