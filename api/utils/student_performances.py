from typing import Sequence

from sqlalchemy import and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.student_performance import StudentPerformance
from pydantic_schemas.student_performance import (
    StudentPerformanceCreate,
    StudentPerformanceQueryParams,
    StudentPerformanceUpdate,
)


async def read_student_performances(
    db: AsyncSession,
    query_params: StudentPerformanceQueryParams,
) -> Sequence[StudentPerformance]:
    filters = []
    if query_params.stud_id:
        filters.append(StudentPerformance.stud_id == query_params.stud_id)
    if query_params.sem_id:
        filters.append(StudentPerformance.sem_id == query_params.sem_id)
    if query_params.total:
        filters.append(StudentPerformance.total == query_params.total)
    if query_params.percentage:
        filters.append(StudentPerformance.percentage == query_params.percentage)
    if query_params.sgpa:
        filters.append(StudentPerformance.sgpa == query_params.sgpa)
    if query_params.min_total:
        filters.append(StudentPerformance.total >= query_params.min_total)
    if query_params.max_total:
        filters.append(StudentPerformance.total <= query_params.max_total)
    if query_params.min_percentage:
        filters.append(StudentPerformance.percentage >= query_params.min_percentage)
    if query_params.max_percentage:
        filters.append(StudentPerformance.percentage <= query_params.max_percentage)
    if query_params.min_sgpa:
        filters.append(StudentPerformance.sgpa >= query_params.min_sgpa)
    if query_params.max_sgpa:
        filters.append(StudentPerformance.sgpa <= query_params.max_sgpa)
    async with db.begin():
        query = select(StudentPerformance).where(and_(*filters))
        result = await db.execute(query)
        student_performances = result.scalars().all()
        return student_performances


async def add_student_performance(
    db: AsyncSession, student_performance: StudentPerformanceCreate
) -> StudentPerformance:
    async with db.begin():
        new_student_performance = StudentPerformance(
            stud_id=student_performance.stud_id,
            sem_id=student_performance.sem_id,
            total=student_performance.total,
            percentage=student_performance.percentage,
            sgpa=student_performance.sgpa,
        )
        db.add(new_student_performance)
        await db.commit()
        return new_student_performance


async def read_student_performance(
    db: AsyncSession, student_performance_id: int
) -> StudentPerformance:
    async with db.begin():
        query = select(StudentPerformance).where(
            StudentPerformance.stud_perf_id == student_performance_id
        )
        result = await db.execute(query)
        student_performance = result.scalars().first()
        return student_performance


async def patch_student_performance(
    db: AsyncSession,
    student_performance_id: int,
    student_performance: StudentPerformanceUpdate,
) -> StudentPerformance:
    async with db.begin():
        update_data = {}
        if student_performance.stud_id:
            update_data["stud_id"] = student_performance.stud_id
        if student_performance.sem_id:
            update_data["sem_id"] = student_performance.sem_id
        if student_performance.total:
            update_data["total"] = student_performance.total
        if student_performance.percentage:
            update_data["percentage"] = student_performance.percentage
        if student_performance.sgpa:
            update_data["sgpa"] = student_performance.sgpa

    if update_data:
        query = (
            update(StudentPerformance)
            .where(StudentPerformance.stud_perf_id == student_performance_id)
            .values(**update_data)
        )
        await db.execute(query)
        await db.commit()

    new_student_performance = await read_student_performance(db, student_performance_id)
    return new_student_performance


async def remove_student_performance(
    db: AsyncSession, student_performance_id: int
) -> StudentPerformance:
    student_performance = await read_student_performance(db, student_performance_id)
    async with db.begin():
        await db.delete(student_performance)
        await db.commit()
        return student_performance
