from typing import Sequence

from sqlalchemy import and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.extraction import Extraction
from db.models.extraction_invalid import ExtractionInvalid
from pydantic_schemas.extraction import (
    ExtractionCreate,
    ExtractionQueryParams,
    ExtractionUpdate,
)
from pydantic_schemas.extraction_invalid import (
    ExtractionInvalidCreate,
    ExtractionInvalidUpdate,
)


async def read_extractions(
    db: AsyncSession,
    query_params: ExtractionQueryParams,
) -> Sequence[Extraction]:
    filters = []
    if query_params.section_id:
        filters.append(Extraction.section_id == query_params.section_id)
    if query_params.sem_id:
        filters.append(Extraction.sem_id == query_params.sem_id)
    if query_params.total_usns:
        filters.append(Extraction.total_usns == query_params.total_usns)
    if query_params.num_completed:
        filters.append(Extraction.num_completed == query_params.num_completed)
    if query_params.num_invalid:
        filters.append(Extraction.num_invalid == query_params.num_invalid)
    if query_params.reattempts:
        filters.append(Extraction.reattempts == query_params.reattempts)
    if query_params.progress:
        filters.append(Extraction.progress == query_params.progress)
    if query_params.completed:
        filters.append(Extraction.completed == query_params.completed)
    if query_params.failed:
        filters.append(Extraction.failed == query_params.failed)
    if query_params.time_taken:
        filters.append(Extraction.time_taken == query_params.time_taken)
    async with db.begin():
        query = select(Extraction).where(and_(*filters))
        result = await db.execute(query)
        extractions = result.scalars().all()
        return extractions


async def add_extraction(db: AsyncSession, extraction: ExtractionCreate) -> Extraction:
    async with db.begin():
        new_extraction = Extraction(
            section_id=extraction.section_id,
            sem_id=extraction.sem_id,
            total_usns=extraction.total_usns,
            num_completed=extraction.num_completed,
            num_invalid=extraction.num_invalid,
            reattempts=extraction.reattempts,
            progress=extraction.progress,
            completed=extraction.completed,
            failed=extraction.failed,
            time_taken=extraction.time_taken,
        )  # type: ignore
        db.add(new_extraction)
        await db.commit()
        return new_extraction


async def read_extraction(db: AsyncSession, extraction_id: int) -> Extraction:
    async with db.begin():
        query = select(Extraction).where(Extraction.extraction_id == extraction_id)
        result = await db.execute(query)
        extraction = result.scalars().first()
        return extraction


async def update_extraction(
    db: AsyncSession,
    extraction_id: int,
    extraction_data: ExtractionUpdate,
) -> Extraction:
    async with db.begin():
        update_data = {}
        if extraction_data.section_id:
            update_data["section_id"] = extraction_data.section_id
        if extraction_data.sem_id:
            update_data["sem_id"] = extraction_data.sem_id
        if extraction_data.total_usns:
            update_data["total_usns"] = extraction_data.total_usns
        if extraction_data.num_completed:
            update_data["num_completed"] = extraction_data.num_completed
        if extraction_data.num_invalid:
            update_data["num_invalid"] = extraction_data.num_invalid
        if extraction_data.reattempts:
            update_data["reattempts"] = extraction_data.reattempts
        if extraction_data.progress:
            update_data["progress"] = extraction_data.progress
        if extraction_data.completed:
            update_data["completed"] = extraction_data.completed
        if extraction_data.failed:
            update_data["failed"] = extraction_data.failed
        if extraction_data.time_taken:
            update_data["time_taken"] = extraction_data.time_taken

        if update_data:
            query = (
                update(Extraction)
                .where(Extraction.extraction_id == extraction_id)
                .values(**update_data)
            )
            await db.execute(query)
            await db.commit()

    new_extraction = await read_extraction(db, extraction_id)
    return new_extraction


async def delete_extraction(db: AsyncSession, extraction_id: int) -> Extraction:
    async with db.begin():
        extraction = await read_extraction(db, extraction_id)
        await db.delete(extraction)
        await db.commit()
        return extraction


async def read_extraction_invalids(db: AsyncSession) -> Sequence[ExtractionInvalid]:
    async with db.begin():
        query = select(ExtractionInvalid)
        result = await db.execute(query)
        extraction_invalids = result.scalars().all()
        return extraction_invalids


async def add_extraction_invalid(
    db: AsyncSession, extraction_invalid: ExtractionInvalidCreate
) -> ExtractionInvalid:
    async with db.begin():
        new_extraction_invalid = ExtractionInvalid(
            extraction_id=extraction_invalid.extraction_id,
            invalid_usns=extraction_invalid.invalid_usns,
            captcha_usns=extraction_invalid.captcha_usns,
            timeout_usns=extraction_invalid.timeout_usns,
        )  # type: ignore
        db.add(new_extraction_invalid)
        await db.commit()
        return new_extraction_invalid


async def read_extraction_invalid(
    db: AsyncSession, invalid_id: int
) -> ExtractionInvalid:
    async with db.begin():
        query = select(ExtractionInvalid).where(
            ExtractionInvalid.invalid_id == invalid_id
        )
        result = await db.execute(query)
        extraction_invalid = result.scalars().first()
        return extraction_invalid


async def update_extraction_invalid(
    db: AsyncSession,
    invalid_id: int,
    extraction_invalid_data: ExtractionInvalidUpdate,
) -> ExtractionInvalid:
    async with db.begin():
        update_data = {}
        if extraction_invalid_data.extraction_id:
            update_data["extraction_id"] = extraction_invalid_data.extraction_id
        if extraction_invalid_data.invalid_usns:
            update_data["invalid_usns"] = extraction_invalid_data.invalid_usns
        if extraction_invalid_data.captcha_usns:
            update_data["captcha_usns"] = extraction_invalid_data.captcha_usns
        if extraction_invalid_data.timeout_usns:
            update_data["timeout_usns"] = extraction_invalid_data.timeout_usns

        if update_data:
            query = (
                update(ExtractionInvalid)
                .where(ExtractionInvalid.invalid_id == invalid_id)
                .values(**update_data)
            )
            await db.execute(query)
            await db.commit()

    new_extraction_invalid = await read_extraction_invalid(db, invalid_id)
    return new_extraction_invalid


async def delete_extraction_invalid(
    db: AsyncSession, invalid_id: int
) -> ExtractionInvalid:
    async with db.begin():
        extraction_invalid = await read_extraction_invalid(db, invalid_id)
        await db.delete(extraction_invalid)
        await db.commit()
        return extraction_invalid
