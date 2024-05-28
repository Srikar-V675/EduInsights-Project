import json
from typing import List

import numpy as np
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.batch import Batch
from db.models.semester import Semester
from db.models.subject import Subject
from pydantic_schemas.extraction import IdentifySubjects, SubjectSchema
from webExtractor.driver import initialise_driver
from webExtractor.scraper import scrape_results

from .scraper_utils import check_url


async def identify_subjects(
    batch_id: int,
    data: IdentifySubjects,
    db: AsyncSession,
) -> List[SubjectSchema]:
    """
    scrape_results status codes reference:
        0: Success
        1: Invalid USN or non-existent USN
        2: Invalid captcha
        3: Connection Timeout
        4: DNS resolution failed
        5: Other WebDriverException
        6: Other Exception
        >10: 10 + reattempts for invalid captcha
        >20: 20 + reattempts for connection timeout
    """

    if not await check_url(data.result_url):
        raise HTTPException(status_code=400, detail="Error: Invalid URL")

    async with db.begin():
        query = select(Batch.start_usn, Batch.end_usn).where(Batch.batch_id == batch_id)
        result = await db.execute(query)
        batch = result.first()

        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")

        if not data.usn or data.usn == "":
            start_usn_str = batch.start_usn[
                7:
            ]  # Get substring from 7th position onward
            end_usn_str = batch.end_usn[7:]

            # Convert the substring to an integer
            start_usn = int(start_usn_str)  # type: ignore
            end_usn = int(end_usn_str)  # type: ignore

            usn = np.random.randint(start_usn, end_usn + 1)
            if usn > 0 and usn < 10:
                usn = "00" + str(usn)
            elif usn >= 10 and usn < 100:
                usn = "0" + str(usn)
            else:
                usn = str(usn)
            usn = batch.start_usn[:7] + usn
        else:
            usn = data.usn

        driver = initialise_driver()
        student_data, status_code = await scrape_results(usn, data.result_url, driver)
        if status_code == 0 or status_code > 10 or status_code > 20:
            student_data = json.loads(student_data)  # type: ignore
            subjects = student_data["Marks"]
            subjects = [subject for subject in subjects]
            subjects = [
                SubjectSchema(
                    **{
                        "sub_code": subject["Subject Code"],
                        "sub_name": subject["Subject Name"],
                        "credits": 0,
                    }
                )
                for subject in subjects
            ]
            return subjects
        else:
            error = ""
            if status_code == 1:
                error = "Invalid USN or non-existent USN"
            elif status_code == 2:
                error = "Invalid captcha"
            elif status_code == 3:
                error = "Connection Timeout"
            elif status_code == 4:
                error = "Connection Refused"
            elif status_code == 5:
                error = "Other WebDriverException"
            elif status_code == 6:
                error = "Other Exception"
            raise HTTPException(
                status_code=500, detail="Error in scraping results: " + error
            )


async def add_subjects(
    batch_id: int,
    subjects: List[SubjectSchema],
    db: AsyncSession,
) -> List[SubjectSchema]:
    async with db.begin():
        query = select(Batch).where(Batch.batch_id == batch_id)
        result = await db.execute(query)
        batch = result.first()

        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")

        query = select(Semester.sem_id).where(
            and_(Semester.batch_id == batch_id, Semester.current == True)
        )  # noqa
        result = await db.execute(query)
        sem_id = result.scalar()

        if not sem_id:
            raise HTTPException(status_code=404, detail="Semester not found")

        try:
            new_subjects = []
            for subject in subjects:
                if subject.credits == 0:
                    raise HTTPException(
                        status_code=422,
                        detail="Credits for subject " + subject.sub_code + " is 0",
                    )
                new_subject = Subject(
                    sub_code=subject.sub_code,
                    sub_name=subject.sub_name,
                    credits=subject.credits,
                    sem_id=sem_id,
                )  # type: ignore
                new_subjects.append(new_subject)

            db.add_all(new_subjects)
            await db.commit()
            return new_subjects
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=422, detail=str(e))
