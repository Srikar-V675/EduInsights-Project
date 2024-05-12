from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DepartmentBase(BaseModel):
    """
    Base Pydantic model for creating or updating a department.

    Attributes:
        dept_name (int): The name of the department.
        password (str): The password for the department.
    """

    dept_name: int
    password: str


class DepartmentCreate(DepartmentBase):
    """
    Pydantic model for creating a new department.

    Inherits attributes from DepartmentBase.
    """

    pass


class DepartmentUpdate(BaseModel):
    dept_name: Optional[int]
    password: Optional[str]


class Department(DepartmentBase):
    """
    Pydantic model representing a department.

    Inherits attributes from DepartmentBase and includes additional attributes for database timestamps.

    Attributes:
        dept_id (int): The unique identifier for the department.
        created_at (datetime): The timestamp indicating when the department was created.
        updated_at (datetime): The timestamp indicating when the department was last updated.

    Config:
        from_attributes (bool): Indicates that the model should be constructed from database attributes.
    """

    dept_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
