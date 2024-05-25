import asyncio
import json
import time
from typing import List

from fastapi import BackgroundTasks, HTTPException
from pydantic import HttpUrl
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from db.models.extraction import Extraction
from db.models.mark import Mark
from db.models.section import Section
from db.models.semester import Semester
from db.models.student import Student
from db.models.subject import Subject
from pydantic_schemas.extraction import ExtractionCreate, ExtractionUpdate
from pydantic_schemas.mark import MarkUpdate
from pydantic_schemas.student import StudentUpdate
from webExtractor.driver import initialise_driver
from webExtractor.scraper import scrape_results

from ..marks import patch_mark
from ..students import patch_student
from .table_utils import add_extraction, update_extraction


async def scrape_section(
    section_id: int,
    result_url: HttpUrl,
    background_tasks: BackgroundTasks,
    session_factory: sessionmaker,
):
    async with session_factory() as db:
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

        query = select(Semester.sem_id).where(
            and_(
                Semester.batch_id == section.batch_id, Semester.current == True
            )  # noqa
        )
        result = await db.execute(query)
        sem_id = result.scalar()

        if not sem_id:
            raise HTTPException(status_code=404, detail="Semester not found")

        prefix_usn = section.start_usn[:7]
        start_usn = int(section.start_usn[7:])
        end_usn = int(section.end_usn[7:])

        total_usns = end_usn - start_usn + 1
        usns = [usn for usn in range(start_usn, end_usn + 1)]

    extraction = ExtractionCreate(
        section_id=section_id,
        sem_id=sem_id,
        total_usns=total_usns,
        num_completed=0,
        num_invalid=0,
        reattempts=0,
        progress=0.0,
        completed=False,
        failed=False,
        time_taken=0.0,
    )
    new_extraction = await add_extraction(db, extraction)
    async with session_factory() as db:
        query = select(Extraction.extraction_id).where(
            Extraction.extraction_id == new_extraction.extraction_id
        )
        result = await db.execute(query)
        extraction_id = result.scalars().first()

    async def process_subsets():
        await scrape_and_store(
            result_url,
            prefix_usn,
            usns,
            section_id,
            sem_id,
            extraction_id,  # type: ignore
            session_factory,
        )

    background_tasks.add_task(process_subsets)

    return {
        "message": "Scraping in progress",
        "extraction_id": extraction_id,
        "start_usn": section.start_usn,
        "end_usn": section.end_usn,
        "number_usns": total_usns,
    }


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
            f"Num completed: {num_completed}, Num invalid: {num_invalid}, Reattempts: {reattempts}, Progress: {progress}, Time taken: {time_taken}"
        )
    await update_extraction(db, extraction_id, new_extraction)
    print(f"Extraction {extraction_id} updated")
    return True


async def scrape_and_store(
    result_url: HttpUrl,  # Changed to str for simplicity
    prefix_usn: str,
    usns: List[int],
    section_id: int,
    sem_id: int,
    extraction_id: int,
    session_factory: sessionmaker,
):
    driver = initialise_driver()
    count = 0
    reattempts = 0
    invalids = 0
    start_time = time.time()

    # Create a new session for this task
    async with session_factory() as db:
        for usn in usns:
            if count == 5:
                await update_extraction_progress(
                    count,
                    invalids,
                    reattempts,
                    time.time() - start_time,
                    extraction_id,
                    db,
                )

                count = 0
                invalids = 0
                reattempts = 0
                start_time = time.time()

            count += 1
            usn = prefix_usn + str(usn).zfill(3)

            async with db.begin():
                query = select(
                    Student.stud_id, Student.usn, Student.stud_name, Student.active
                ).where(and_(Student.usn == usn, Student.section_id == section_id))
                result = await db.execute(query)
                student = result.first()

            if student and not student.active:
                invalids += 1
                continue

            stud_id = student.stud_id  # type: ignore
            isActive = student.active  # type: ignore
            student_data, status_code = await scrape_results(usn, result_url, driver)
            if status_code == 0 or status_code > 10 or status_code > 20:
                student_data = json.loads(student_data)  # type: ignore
                if status_code > 10:
                    reattempts += status_code - 10
                elif status_code > 20:
                    reattempts += status_code - 20
            else:
                # error = ""
                if status_code == 1:
                    isActive = False
                    # error = f"Invalid USN or non-existent USN: {usn}"
                    invalids += 1
                # elif status_code == 2:
                #     # error = "Invalid captcha"
                # elif status_code == 3:
                #     # error = "Connection Timeout"
                # elif status_code == 4:
                #     # error = "DNS resolution failed"
                # elif status_code == 5:
                #     error = "Other WebDriverException"
                # elif status_code == 6:
                #     error = "Other Exception"
                # elif status_code == 7:
                #     error = "Connection refused"
                continue

            stud_name = student_data["Name"]
            marks = student_data["Marks"]

            # Update student data
            if student.stud_name != stud_name and not isActive:  # type: ignore
                await patch_student(db, student.stud_id, StudentUpdate(stud_name=stud_name[1:], active=True))  # type: ignore
            elif student.stud_name != stud_name:  # type: ignore
                await patch_student(db, student.stud_id, StudentUpdate(stud_name=stud_name[1:]))  # type: ignore
            elif not isActive:
                await patch_student(db, student.stud_id, StudentUpdate(active=True))  # type: ignore

            # Add marks
            new_marks = []
            for mark in marks:
                subject_code = mark["Subject Code"]
                internal = mark["INT"]
                external = mark["EXT"]
                total = mark["TOT"]
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

                async with db.begin():
                    query = select(Subject.subject_id).where(
                        Subject.sub_code == subject_code
                    )
                    result = await db.execute(query)
                    subject_id = result.scalar()

                async with db.begin():
                    query = select(Mark.mark_id).where(
                        and_(Mark.stud_id == stud_id, Mark.subject_id == subject_id)
                    )
                    result = await db.execute(query)
                    existing_mark = result.first()

                if existing_mark:
                    update_mark = MarkUpdate(
                        internal=internal,
                        external=external,
                        total=total,
                        result=result_code,
                        grade=grade,
                    )
                    await patch_mark(db, existing_mark.mark_id, update_mark)

                else:
                    new_mark = Mark(
                        stud_id=stud_id,
                        subject_id=subject_id,  # type: ignore
                        section_id=section_id,
                        internal=int(internal),
                        external=int(external),
                        total=int(total),
                        result=result_code,
                        grade=grade,
                    )
                    new_marks.append(new_mark)  # noqa

            async with db.begin():
                db.add_all(new_marks)
                await db.commit()
        if count > 0:
            await update_extraction_progress(
                count,
                invalids,
                reattempts,
                time.time() - start_time,
                extraction_id,
                db,
            )

        driver.quit()  # type: ignore
        await asyncio.sleep(1)
        return True
