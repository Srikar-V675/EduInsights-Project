from typing import List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.students import (
    add_student,
    patch_student,
    read_student,
    read_students,
    remove_student,
)
from db.db_setup import get_db
from pydantic_schemas.student import (
    Student,
    StudentCreate,
    StudentQueryParams,
    StudentUpdate,
)

router = fastapi.APIRouter()


# Route to retrieve all students
@router.get("", response_model=List[Student])
async def get_students(
    query_params: StudentQueryParams = Depends(), db: AsyncSession = Depends(get_db)
):
    students = await read_students(db, query_params)
    return students


# Route to create a new student
@router.post("", response_model=Student, status_code=201)
async def create_new_student(
    student: StudentCreate, db: AsyncSession = Depends(get_db)
):
    student = await add_student(db=db, student=student)
    return student


# Route to retrieve a specific student by its ID
@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await read_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# Route to update a specific student by its ID
@router.patch("/{student_id}", response_model=Student)
async def update_student(
    student_id: int, student_data: StudentUpdate, db: AsyncSession = Depends(get_db)
):
    student = await read_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    new_student = await patch_student(db, student_id, student_data)
    return new_student


# Route to delete a specific student by its ID
@router.delete("/{student_id}", response_model=Student)
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await read_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    student = await remove_student(db, student_id)
    return student
