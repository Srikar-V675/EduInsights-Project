from typing import Sequence

from sqlalchemy import and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.student import Student
from pydantic_schemas.student import StudentCreate, StudentQueryParams, StudentUpdate


async def read_students(
    db: AsyncSession,
    query_params: StudentQueryParams,
) -> Sequence[Student]:
    filters = []
    if query_params.batch_id:
        filters.append(Student.batch_id == query_params.batch_id)
    if query_params.section_id:
        filters.append(Student.section_id == query_params.section_id)
    if query_params.current_sem:
        filters.append(Student.current_sem == query_params.current_sem)
    if query_params.active is not None:
        filters.append(Student.active == query_params.active)
    if query_params.min_cgpa:
        filters.append(Student.cgpa >= query_params.min_cgpa)
    if query_params.max_cgpa:
        filters.append(Student.cgpa <= query_params.max_cgpa)
    if query_params.cgpa:
        filters.append(Student.cgpa == query_params.cgpa)
    if query_params.usn:
        filters.append(Student.usn == query_params.usn)
    if query_params.stud_name:
        filters.append(Student.stud_name == query_params.stud_name)
    async with db.begin():
        query = select(Student).where(and_(*filters))
        result = await db.execute(query)
        students = result.scalars().all()
        return students


async def read_student(db: AsyncSession, student_id: int) -> Student:
    async with db.begin():
        query = select(Student).filter(Student.stud_id == student_id)
        result = await db.execute(query)
        student = result.scalar_one_or_none()
        return student


async def add_student(db: AsyncSession, student: StudentCreate) -> Student:
    async with db.begin():
        new_student = Student(
            batch_id=student.batch_id,
            usn=student.usn,
            section_id=student.section_id,
            stud_name=student.stud_name,
            cgpa=student.cgpa,
            active=student.active,
            current_sem=student.current_sem,
        )
        db.add(new_student)
        await db.commit()
        return new_student


async def patch_student(
    db: AsyncSession, student_id: int, student_data: StudentUpdate
) -> Student:
    async with db.begin():
        update_data = {}
        if student_data.batch_id:
            update_data["batch_id"] = student_data.batch_id
        if student_data.usn:
            update_data["usn"] = student_data.usn
        if student_data.section_id:
            update_data["section_id"] = student_data.section_id
        if student_data.stud_name:
            update_data["stud_name"] = student_data.stud_name
        if student_data.cgpa:
            update_data["cgpa"] = student_data.cgpa
        if student_data.active is not None:
            update_data["active"] = student_data.active
        if student_data.current_sem:
            update_data["current_sem"] = student_data.current_sem

        if update_data:
            query = (
                update(Student)
                .where(Student.stud_id == student_id)
                .values(**update_data)
            )
            await db.execute(query)
            await db.commit()

    new_student = await read_student(db, student_id)
    return new_student


async def remove_student(db: AsyncSession, student_id: int) -> Student:
    student = await read_student(db, student_id)
    async with db.begin():
        await db.delete(student)
        await db.commit()
    return student
