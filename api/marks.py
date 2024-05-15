from typing import Sequence

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.marks import add_mark, patch_mark, read_mark, read_marks, remove_mark
from db.db_setup import get_db
from pydantic_schemas.mark import Mark, MarkCreate, MarkUpdate

router = fastapi.APIRouter()


# Route to retrieve all marks
@router.get("", response_model=Sequence[Mark])
async def get_marks(db: AsyncSession = Depends(get_db)):
    marks = await read_marks(db)
    return marks


# Route to create a new mark
@router.post("", response_model=Mark, status_code=201)
async def create_new_mark(mark: MarkCreate, db: AsyncSession = Depends(get_db)):
    mark = await add_mark(db=db, mark=mark)
    return mark


# Route to retrieve a specific mark by its ID
@router.get("/{mark_id}", response_model=Mark)
async def get_mark(mark_id: int, db: AsyncSession = Depends(get_db)):
    mark = await read_mark(db, mark_id)
    if mark is None:
        raise HTTPException(status_code=404, detail="Mark not found")
    return mark


# Route to update a specific mark by its ID
@router.patch("/{mark_id}", response_model=Mark)
async def update_mark(
    mark_id: int, mark_data: MarkUpdate, db: AsyncSession = Depends(get_db)
):
    mark = await read_mark(db, mark_id)
    if mark is None:
        raise HTTPException(status_code=404, detail="Mark not found")
    new_mark = await patch_mark(db, mark_id, mark_data)
    return new_mark


# Route to delete a specific mark by its ID
@router.delete("/{mark_id}", response_model=Mark)
async def delete_mark(mark_id: int, db: AsyncSession = Depends(get_db)):
    mark = await read_mark(db, mark_id)
    if mark is None:
        raise HTTPException(status_code=404, detail="Mark not found")
    mark = await remove_mark(db, mark_id)
    return mark
