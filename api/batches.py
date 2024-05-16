from typing import List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_setup import get_db
from pydantic_schemas.batch import Batch, BatchCreate, BatchQueryParams, BatchUpdate

from .utils.batches import (
    add_batch,
    patch_batch,
    read_batch,
    read_batches,
    remove_batch,
)

router = fastapi.APIRouter()


@router.get("", response_model=List[Batch])
async def get_batches(
    query_params: BatchQueryParams = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all batches from the database.

    Args:
        db (AsyncSession): An asynchronous database session.

    Returns:
        List[Batch]: A list of Batch objects representing all batches in the database.
    """
    batches = await read_batches(db, query_params)
    return batches


@router.post("", response_model=Batch, status_code=201)
async def create_new_batch(batch: BatchCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new batch and add it to the database.

    Args:
        batch (BatchCreate): Data for the new batch.
        db (AsyncSession): An asynchronous database session.

    Returns:
        Batch: The newly created batch.
    """
    return await add_batch(db=db, batch=batch)


@router.get("/{batch_id}", response_model=Batch)
async def get_batch(batch_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a batch from the database by its ID.

    Args:
        batch_id (int): The ID of the batch to retrieve.
        db (AsyncSession): An asynchronous database session.

    Returns:
        Batch: The retrieved batch, if found.

    Raises:
        HTTPException: If the batch with the specified ID is not found, raises 404 error.
    """
    batch = await read_batch(batch_id=batch_id, db=db)
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found.")
    return batch


@router.patch("/{batch_id}", response_model=Batch)
async def update_batch(
    batch_id: int, batch_data: BatchUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Update a batch in the database.

    Args:
        batch_id (int): The ID of the batch to update.
        batch (BatchUpdate): Data to update the batch with.
        db (AsyncSession): An asynchronous database session.

    Returns:
        Batch: The updated batch.

    Raises:
        HTTPException: If the batch with the specified ID is not found, raises 404 error.
    """
    existing_batch = await read_batch(batch_id=batch_id, db=db)
    if existing_batch is None:
        raise HTTPException(status_code=404, detail="Batch not found.")
    new_batch = await patch_batch(batch_id=batch_id, batch_data=batch_data, db=db)
    return new_batch


@router.delete("/{batch_id}", response_model=Batch)
async def delete_batch(batch_id: int, db: AsyncSession = Depends(get_db)):
    batch = await read_batch(batch_id=batch_id, db=db)
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found.")
    del_batch = await remove_batch(batch_id=batch_id, db=db)
    return del_batch
