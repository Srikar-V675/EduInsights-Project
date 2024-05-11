from typing import List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.departments import (
    add_department,
    read_department,
    read_department_batches,
    read_departments,
)
from db.db_setup import get_db
from pydantic_schemas.batch import Batch
from pydantic_schemas.department import Department, DepartmentCreate

router = fastapi.APIRouter()


@router.get("", response_model=List[Department])
async def get_departments(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all departments from the database.

    Args:
        db (AsyncSession): An asynchronous database session.

    Returns:
        List[Department]: A list of Department objects representing all departments in the database.
    """
    depts = await read_departments(db)
    return depts


@router.post("", response_model=Department, status_code=201)
async def create_new_department(
    department: DepartmentCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new department and add it to the database.

    Args:
        department (DepartmentCreate): Data for the new department.
        db (AsyncSession): An asynchronous database session.

    Returns:
        Department: The newly created department.
    """
    return await add_department(db=db, department=department)


@router.get("/{dept_id}", response_model=Department)
async def get_department(dept_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a department from the database by its ID.

    Args:
        dept_id (int): The ID of the department to retrieve.
        db (AsyncSession): An asynchronous database session.

    Returns:
        Department: The retrieved department, if found.

    Raises:
        HTTPException: If the department with the specified ID is not found, raises 404 error.
    """
    dept = await read_department(db=db, dept_id=dept_id)
    if dept is None:
        raise HTTPException(status_code=404, detail="Department not found.")
    return dept


@router.get("/{dept_id}/batches", response_model=List[Batch])
async def get_department_batches(dept_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all batches associated with a department from the database.

    Args:
        dept_id (int): The ID of the department.
        db (AsyncSession): An asynchronous database session.

    Returns:
        List[Batch]: A list of Batch objects representing all batches associated with the department.

    Raises:
        HTTPException: If the department with the specified ID is not found, raises 404 error.
    """
    dept = await read_department(db=db, dept_id=dept_id)
    if dept is None:
        raise HTTPException(status_code=404, detail="Department not found.")
    batches = await read_department_batches(db=db, dept_id=dept_id)
    return batches
