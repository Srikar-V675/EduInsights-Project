from typing import List

import requests
from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from db.models.extraction import Extraction
from db.models.mark import Mark
from db.models.section import Section
from db.models.semester import Semester
from db.models.student import Student
from db.models.subject import Subject
from pydantic_schemas.extraction import ExtractionCreate, ExtractionUpdate
from pydantic_schemas.mark import MarkUpdate

from ..marks import patch_mark
from .table_utils import add_extraction, update_extraction


async def check_url(
    url: str,
) -> bool:
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e, flush=True)
        return False
    return True


async def check_get_section(
    section_id: int,
    session: sessionmaker,
) -> Section:
    async with session() as db:
        query = select(
            Section.section_id,
            Section.batch_id,
            Section.num_students,
            Section.start_usn,
            Section.end_usn,
        ).where(Section.section_id == section_id)
        result = await db.execute(query)
        section = result.first()
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")
    return section


async def check_get_semester(
    batch_id: int,
    session: sessionmaker,
) -> Semester:
    async with session() as db:
        query = select(Semester.sem_id).where(
            and_(Semester.batch_id == batch_id, Semester.current == True)  # noqa
        )
        result = await db.execute(query)
        semester = result.first()
        if not semester:
            raise HTTPException(status_code=404, detail="Semester not found")
    return semester


async def create_get_extraction(
    extraction: ExtractionCreate,
    session: sessionmaker,
) -> int:
    async with session() as db:
        new_extraction = await add_extraction(db, extraction)
        query = select(Extraction.extraction_id).where(
            Extraction.extraction_id == new_extraction.extraction_id
        )
        result = await db.execute(query)
        extraction_id = result.scalars().first()
    return extraction_id


async def update_extraction_progress(
    count: int,
    invalid: int,
    reattempts: int,
    time_taken: float,
    extraction_id: int,
    db: AsyncSession,
) -> bool:
    async with db.begin():
        query = select(
            Extraction.total_usns,
            Extraction.num_completed,
            Extraction.num_invalid,
            Extraction.reattempts,
            Extraction.progress,
            Extraction.time_taken,
        ).where(Extraction.extraction_id == extraction_id)
        result = await db.execute(query)
        extraction = result.first()

        num_completed = extraction.num_completed + count  # type: ignore
        num_invalid = extraction.num_invalid + invalid  # type: ignore
        reattempts = extraction.reattempts + reattempts  # type: ignore
        progress = round((num_completed / extraction.total_usns) * 100, 2)  # type: ignore
        time_taken = float(extraction.time_taken) + time_taken  # type: ignore
        completed = False
        # time_taken_new = str(time_taken)
        if progress == 100.0:
            completed = True

        new_extraction = ExtractionUpdate(
            num_completed=num_completed,
            num_invalid=num_invalid,
            reattempts=reattempts,
            progress=progress,
            completed=completed,
            time_taken=time_taken,
        )
        print(
            f"Num completed: {num_completed}, Num invalid: {num_invalid}, Reattempts: {reattempts}, Progress: {progress}, Time taken: {time_taken}",
            flush=True,
        )
    await update_extraction(db, extraction_id, new_extraction)
    print(f"Extraction {extraction_id} updated")
    return True


async def check_get_student(
    usn: str,
    section_id: int,
    db: AsyncSession,
) -> Student:
    async with db.begin():
        query = select(
            Student.stud_id, Student.usn, Student.stud_name, Student.active
        ).where(and_(Student.usn == usn, Student.section_id == section_id))
        result = await db.execute(query)
        student = result.first()
    return student


async def process_marks(
    marks: dict,
    stud_id: int,
    section_id: int,
    session: sessionmaker,
):
    async with session() as db:

        new_marks = []
        for mark in marks:
            subject_code = mark["Subject Code"]
            internal = int(mark["INT"])
            external = int(mark["EXT"])
            total = int(mark["TOT"])
            result_code = mark["Result"]
            grade = ""
            if result_code == "P":
                if int(total) >= 75:
                    grade = "FCD"
                elif int(total) >= 60:
                    grade = "FC"
                else:
                    grade = "SC"
            elif result_code == "F":
                grade = "FAIL"
            elif result_code == "A":
                grade = "ABSENT"

            subject_id = await check_get_subject_id(subject_code, db)

            mark_id = await check_mark_exists(stud_id, subject_id, section_id, db)

            if mark_id:
                update_mark = MarkUpdate(
                    internal=internal,
                    external=external,
                    total=total,
                    result=result_code,
                    grade=grade,
                )
                await patch_mark(db, mark_id.mark_id, update_mark)

            else:
                new_mark = Mark(
                    stud_id=stud_id,
                    subject_id=subject_id,
                    section_id=section_id,
                    internal=internal,
                    external=external,
                    total=total,
                    result=result_code,
                    grade=grade,
                )  # type: ignore
                new_marks.append(new_mark)

        if new_marks:
            await batch_add_marks(new_marks, db)


async def check_get_subject_id(
    subject_code: str,
    db: AsyncSession,
) -> int:
    async with db.begin():
        query = select(Subject.subject_id).where(Subject.sub_code == subject_code)
        result = await db.execute(query)
        subject_id = result.scalar()
    return subject_id


async def check_mark_exists(
    stud_id: int,
    subject_id: int,
    section_id: int,
    db: AsyncSession,
) -> Mark:
    async with db.begin():
        query = select(Mark.mark_id).where(
            and_(
                Mark.stud_id == stud_id,
                Mark.subject_id == subject_id,
                Mark.section_id == section_id,
            )
        )
        result = await db.execute(query)
        mark_id = result.first()
    return mark_id


async def batch_add_marks(
    new_marks: List[Mark],
    db: AsyncSession,
):
    async with db.begin():
        db.add_all(new_marks)
        await db.commit()
