from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

VALID_DEPT_NAMES = {"CSE", "ISE", "AIML", "ECE", "EEE", "MECH", "CIVIL"}


class DepartmentBase(BaseModel):
    """
    Base Pydantic model for creating or updating a department.

    Attributes:
        dept_name (int): The name of the department.
        password (str): The password for the department.
    """

    dept_name: str
    password: str

    @validator("dept_name")
    def validate_dept_name(cls, dept_name: str) -> str:
        """
        Validates the department name.

        Args:
            dept_name (str): The name of the department.

        Returns:
            str: The validated department name.

        Raises:
            ValueError: If the department name is not valid.
        """
        if dept_name not in VALID_DEPT_NAMES:
            raise ValueError("Invalid department name")
        return dept_name


class DepartmentCreate(DepartmentBase):
    """
    Pydantic model for creating a new department.

    Inherits attributes from DepartmentBase.
    """

    pass


class DepartmentUpdate(BaseModel):
    dept_name: Optional[str]
    password: Optional[str]

    @validator("dept_name", pre=True, always=True)
    def validate_dept_name(cls, dept_name: Optional[str]) -> Optional[str]:
        """
        Validates the department name.

        Args:
            dept_name (Optional[str]): The name of the department.

        Returns:
            Optional[str]: The validated department name.

        Raises:
            ValueError: If the department name is not valid.
        """
        if dept_name and dept_name not in VALID_DEPT_NAMES:
            raise ValueError("Invalid department name")
        return dept_name


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
