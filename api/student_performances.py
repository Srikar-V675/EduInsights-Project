from typing import List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.student_performances import (
    add_student_performance,
    patch_student_performance,
    read_student_performance,
    read_student_performances,
    remove_student_performance,
)
from db.db_setup import get_db
from pydantic_schemas.student_performance import (
    StudentPerformance,
    StudentPerformanceCreate,
    StudentPerformanceQueryParams,
    StudentPerformanceUpdate,
)

router = fastapi.APIRouter()


# Route to retrieve all student performances
@router.get("", response_model=List[StudentPerformance])
async def get_student_performances(
    query_params: StudentPerformanceQueryParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    student_performances = await read_student_performances(db, query_params)
    return student_performances


# Route to create a new student performance
@router.post("", response_model=StudentPerformance, status_code=201)
async def create_new_student_performance(
    student_performance: StudentPerformanceCreate, db: AsyncSession = Depends(get_db)
):
    student_performance = await add_student_performance(
        db=db, student_performance=student_performance
    )
    return student_performance


# Route to retrieve a specific student performance by its ID
@router.get("/{student_performance_id}", response_model=StudentPerformance)
async def get_student_performance(
    student_performance_id: int, db: AsyncSession = Depends(get_db)
):
    student_performance = await read_student_performance(db, student_performance_id)
    if student_performance is None:
        raise HTTPException(status_code=404, detail="Student performance not found")
    return student_performance


# Route to update a specific student performance by its ID
@router.patch("/{student_performance_id}", response_model=StudentPerformance)
async def update_student_performance(
    student_performance_id: int,
    student_performance_data: StudentPerformanceUpdate,
    db: AsyncSession = Depends(get_db),
):
    student_performance = await read_student_performance(db, student_performance_id)
    if student_performance is None:
        raise HTTPException(status_code=404, detail="Student performance not found")
    new_student_performance = await patch_student_performance(
        db, student_performance_id, student_performance_data
    )
    return new_student_performance


# Route to delete a specific student performance by its ID
@router.delete("/{student_performance_id}")
async def delete_student_performance(
    student_performance_id: int, db: AsyncSession = Depends(get_db)
):
    student_performance = await read_student_performance(db, student_performance_id)
    if student_performance is None:
        raise HTTPException(status_code=404, detail="Student performance not found")
    removed_student_performance = await remove_student_performance(
        db, student_performance_id
    )
    return removed_student_performance
