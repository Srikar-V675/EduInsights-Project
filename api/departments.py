from typing import List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.departments import (
    add_department,
    patch_department,
    read_department,
    read_departments,
    remove_department,
)
from db.db_setup import get_db
from pydantic_schemas.department import Department, DepartmentCreate, DepartmentUpdate

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

    Note:
        Allowed dept_name's:
            - 'CSE'
            - 'ISE'
            - 'AIML'
            - 'ECE'
            - 'EEE'
            - 'MECH'
            - 'CIVIL'
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


@router.patch("/{dept_id}", response_model=Department)
async def update_department(
    dept_id: int, department_data: DepartmentUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Updates a department with the given department_id.

    Attributes:
        dept_id (int): The unique identifier of the department to be updated.
        department_data (DepartmentUpdate): The data containing the fields to be updated for the department.
        db (AsyncSession): The asynchronous session to interact with the database.

    Returns:
        Department: The updated department object.

    Raises:
        HTTPException: If the department with the given department_id is not found (status code 404).

    Note:
        Allowed dept_name's: 'CSE', 'ISE', 'AIML', 'ECE', 'EEE', 'MECH', 'CIVIL'
    """
    # Read the department from the database
    dept = await read_department(db=db, dept_id=dept_id)
    if dept is None:
        raise HTTPException(status_code=404, detail="Department not found.")

    # Call the patch_department function to update the department
    new_dept = await patch_department(
        db=db, dept_id=dept_id, department_data=department_data
    )
    return new_dept


@router.delete("/{dept_id}", response_model=Department)
async def delete_department(dept_id: int, db: AsyncSession = Depends(get_db)):
    """
    Deletes a department with the given department_id.

    Attributes:
        dept_id (int): The unique identifier of the department to be deleted.
        db (AsyncSession): The asynchronous session to interact with the database.

    Returns:
        Department: The deleted department object.

    Raises:
        HTTPException: If the department with the given department_id is not found (status code 404).
    """
    # Read the department from the database
    dept = await read_department(db=db, dept_id=dept_id)
    if dept is None:
        raise HTTPException(status_code=404, detail="Department not found.")

    # Call the remove_department function to delete the department
    del_dept = await remove_department(db=db, dept_id=dept_id)
    return del_dept
