import asyncio
import json
import time
from typing import List

from fastapi import BackgroundTasks, HTTPException
from pydantic import HttpUrl
from sqlalchemy.orm import sessionmaker

from pydantic_schemas.extraction import ExtractionCreate
from pydantic_schemas.extraction_invalid import ExtractionInvalidCreate
from pydantic_schemas.student import StudentUpdate
from webExtractor.driver import initialise_driver
from webExtractor.scraper import scrape_results

from ..students import patch_student
from .scraper_utils import (
    check_get_section,
    check_get_semester,
    check_get_student,
    check_url,
    create_get_extraction,
    create_get_extraction_invalid,
    process_marks,
    update_extraction_invalid_usns,
    update_extraction_progress,
)


async def scrape_section(
    section_id: int,
    result_url: HttpUrl,
    background_tasks: BackgroundTasks,
    session_factory: sessionmaker,
):

    if not await check_url(str(result_url)):
        raise HTTPException(status_code=400, detail="Invalid URL")

    section = await check_get_section(section_id, session_factory)

    semester = await check_get_semester(section.batch_id, session_factory)

    prefix_usn = section.start_usn[:7]
    start_usn = int(section.start_usn[7:])
    end_usn = int(section.end_usn[7:])

    total_usns = end_usn - start_usn + 1
    usns = [usn for usn in range(start_usn, end_usn + 1)]

    extraction = ExtractionCreate(
        section_id=section_id,
        sem_id=semester.sem_id,  # type: ignore
        total_usns=total_usns,
        num_completed=0,
        num_invalid=0,
        num_captcha=0,
        num_timeout=0,
        reattempts=0,
        progress=0.0,
        completed=False,
        failed=False,
        time_taken=0.0,
    )

    extraction_id = await create_get_extraction(extraction, session_factory)

    extraction_invalid = ExtractionInvalidCreate(
        extraction_id=extraction_id,
        invalid_usns="",
        captcha_usns="",
        timeout_usns="",
    )

    invalid_id = await create_get_extraction_invalid(
        extraction_invalid, session_factory
    )

    async def process_subsets():
        await scrape_and_store(
            result_url,
            prefix_usn,
            usns,
            section_id,
            semester.sem_id,
            extraction_id,  # type: ignore
            invalid_id,  # type: ignore
            session_factory,
        )

    background_tasks.add_task(process_subsets)

    return {
        "message": "Scraping in progress",
        "extraction_id": extraction_id,
        "extraction_invalid_id": invalid_id,
        "start_usn": section.start_usn,
        "end_usn": section.end_usn,
        "number_usns": total_usns,
    }


async def scrape_and_store(
    result_url: HttpUrl,  # Changed to str for simplicity
    prefix_usn: str,
    usns: List[int],
    section_id: int,
    sem_id: int,
    extraction_id: int,
    invalid_id: int,
    session_factory: sessionmaker,
):
    driver = initialise_driver()
    count = 0
    reattempts = 0
    invalids = 0
    captchas = 0
    timeouts = 0
    start_time = time.time()
    invalid_usns = []
    captcha_usns = []
    timeout_usns = []

    # Create a new session for this task
    async with session_factory() as db:
        for usn in usns:
            if count == 5:
                await update_extraction_progress(
                    count,
                    invalids,
                    captchas,
                    timeouts,
                    reattempts,
                    time.time() - start_time,
                    extraction_id,
                    db,
                )

                count = 0
                invalids = 0
                reattempts = 0
                captchas = 0
                timeouts = 0
                start_time = time.time()

            count += 1
            usn = prefix_usn + str(usn).zfill(3)

            student = await check_get_student(usn, section_id, db)

            if student and not student.active:
                invalids += 1
                continue

            stud_id = student.stud_id  # type: ignore
            student_data, status_code = await scrape_results(usn, result_url, driver)
            # reminder: create a function for below if and else
            if status_code == 0 or status_code > 10 or status_code > 20:
                student_data = json.loads(student_data)  # type: ignore
                if status_code > 10:
                    reattempts += status_code - 10
                elif status_code > 20:
                    reattempts += status_code - 20
            else:
                if status_code == 1:
                    invalids += 1
                    invalid_usns.append(usn)
                    student_new = await patch_student(
                        db, student.stud_id, StudentUpdate(active=False)
                    )
                    print("Invalid student active:", student_new.active, flush=True)
                elif status_code == 2:
                    reattempts += 3
                    captchas += 1
                    captcha_usns.append(usn)
                elif status_code == 3:
                    reattempts += 3
                    timeouts += 1
                    timeout_usns.append(usn)
                elif status_code == 4:
                    reattempts += 3
                continue

            stud_name = student_data["Name"]
            marks = student_data["Marks"]

            # Update student data
            if student.stud_name != stud_name[1:]:  # type: ignore
                await patch_student(db, student.stud_id, StudentUpdate(stud_name=stud_name[1:]))  # type: ignore

            await process_marks(marks, stud_id, section_id, session_factory)

        print("Invalid usns: ", invalid_usns, flush=True)

        if count > 0:
            await update_extraction_progress(
                count,
                invalids,
                captchas,
                timeouts,
                reattempts,
                time.time() - start_time,
                extraction_id,
                db,
            )

        await update_extraction_invalid_usns(
            invalid_id,
            invalid_usns,
            captcha_usns,
            timeout_usns,
            db,
        )

        driver.quit()  # type: ignore
        await asyncio.sleep(1)
        return True
