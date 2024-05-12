from typing import Optional, Sequence

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.batch import Batch
from db.models.department import Department
from pydantic_schemas.department import DepartmentCreate, DepartmentUpdate


async def read_departments(db: AsyncSession) -> Sequence[Department]:
    """
    Retrieve all departments from the database.

    Args:
        db (AsyncSession): An asynchronous database session.

    Returns:
        List[Department]: A sequence of Department objects representing all departments in the database.
    """
    async with db.begin():
        query = select(Department)
        result = await db.execute(query)
        departments = result.scalars().all()
        return departments


async def add_department(db: AsyncSession, department: DepartmentCreate) -> Department:
    """
    Add a new department to the database.

    Args:
        db (AsyncSession): An asynchronous database session.
        department (DepartmentCreate): Data for the new department.

    Returns:
        Department: The newly added department.
    """
    async with db.begin():
        new_dept = Department(
            dept_name=department.dept_name, password=department.password
        )
        db.add(new_dept)
        await db.commit()
        return new_dept


async def patch_department(
    db: AsyncSession, dept_id: int, department_data: DepartmentUpdate
) -> Department:
    """
    Updates a department with the given department_id.

    Attributes:
        db (AsyncSession): The asynchronous session to interact with the database.
        dept_id (int): The unique identifier of the department to be updated.
        department_data (DepartmentUpdate): The data containing the fields to be updated for the department.

    Returns:
        Department: The updated department object.

    Raises:
        None
    """
    # Read the department from the database
    # department = await read_department(db=db, dept_id=dept_id)

    # Begin a transaction
    async with db.begin():
        update_data = {}
        if department_data.dept_name:
            update_data["dept_name"] = department_data.dept_name
        if department_data.password:
            update_data["password"] = department_data.password

        # If there are fields to update, execute the update query
        if update_data:
            query = (
                update(Department)
                .where(Department.dept_id == dept_id)
                .values(**update_data)
            )
            await db.execute(query)
            await db.commit()

    # Read the updated department from the database
    new_dept = await read_department(db=db, dept_id=dept_id)
    return new_dept


async def remove_department(db: AsyncSession, dept_id: int) -> Department:
    """
    Removes a department with the given department_id.

    Attributes:
        db (AsyncSession): The asynchronous session to interact with the database.
        dept_id (int): The unique identifier of the department to be removed.

    Returns:
        Department: The removed department object.

    Raises:
        None
    """
    # Read the department from the database
    department = await read_department(db=db, dept_id=dept_id)

    # Begin a transaction
    async with db.begin():
        # Delete the department from the database
        await db.delete(department)
        await db.commit()

    return department


async def read_department(db: AsyncSession, dept_id: int) -> Optional[Department]:
    """
    Retrieve a department from the database by its ID.

    Args:
        db (AsyncSession): An asynchronous database session.
        dept_id (int): The ID of the department to retrieve.

    Returns:
        Optional[Department]: The retrieved department, if found; otherwise, None.
    """
    async with db.begin():
        query = select(Department).where(Department.dept_id == dept_id)
        result = await db.execute(query)
        department = result.scalar_one_or_none()
        return department


async def read_department_batches(db: AsyncSession, dept_id: int) -> Sequence[Batch]:
    """
    Retrieve all batches associated with a department from the database.

    Args:
        db (AsyncSession): An asynchronous database session.
        dept_id (int): The ID of the department.

    Returns:
        Sequence[Batch]: A sequence of Batch objects representing all batches associated with the department.
    """
    async with db.begin():
        query = select(Batch).where(Batch.dept_id == dept_id)
        result = await db.execute(query)
        batches = result.scalars().all()
        return batches
