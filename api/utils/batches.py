from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.batch import Batch
from pydantic_schemas.batch import BatchCreate


async def read_batches(db: AsyncSession) -> Sequence[Batch]:
    """
    Retrieve all batches from the database.

    Args:
        db (AsyncSession): An asynchronous database session.

    Returns:
        Sequence[Batch]: sequence of batches retrieved of type Batch
    """
    async with db.begin():
        query = select(Batch)
        result = await db.execute(query)
        batches = result.scalars().all()
        return batches


async def add_batch(db: AsyncSession, batch: BatchCreate) -> Batch:
    """
    Add a new batch to the database.

    Args:
        db (AsyncSession): An asynchronous database session.
        batch (BatchCreate): Data for the new batch.

    Returns:
        Batch: The newly added batch.
    """
    async with db.begin():
        new_batch = Batch(
            dept_id=batch.dept_id,
            batch_name=batch.batch_name,
            batch_year=batch.batch_year,
            scheme=batch.scheme,
            num_students=batch.num_students,
        )
        db.add(new_batch)
        await db.commit()
        return new_batch


async def read_batch(db: AsyncSession, batch_id: int) -> Batch:
    """
    Retrieve a batch from the database by its ID.

    Args:
        db (AsyncSession): An asynchronous database session.
        batch_id (int): The ID of the batch to retrieve.

    Returns:
        Batch: The retrieved batch, if found; otherwise, None.
    """
    async with db.begin():
        query = select(Batch).where(Batch.batch_id == batch_id)
        result = await db.execute(query)
        batch = result.scalar_one_or_none()
        return batch
