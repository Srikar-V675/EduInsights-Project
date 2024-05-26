from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse

from api import (
    batches,
    departments,
    extractions,
    marks,
    sections,
    semesters,
    student_performances,
    students,
    subjects,
)
from celery_worker import create_task

api = FastAPI(
    title="EduInsights API",
    description="API for managing VTU results, analysis and extraction.",
    version="0.1.0",
)


@api.post("/celery-test")
def run_task(data=Body(...)):
    amount = int(data["amount"])
    x = int(data["x"])
    y = int(data["y"])
    task = create_task.delay(amount, x, y)
    return JSONResponse({"Result": task.get()})


api.include_router(departments.router, prefix="/departments", tags=["Department APIs"])
api.include_router(batches.router, prefix="/batches", tags=["Batch APIs"])
api.include_router(semesters.router, prefix="/semesters", tags=["Semester APIs"])
api.include_router(sections.router, prefix="/sections", tags=["Section APIs"])
api.include_router(subjects.router, prefix="/subjects", tags=["Subject APIs"])
api.include_router(students.router, prefix="/students", tags=["Student APIs"])
api.include_router(marks.router, prefix="/marks", tags=["Marks APIs"])
api.include_router(
    student_performances.router,
    prefix="/student-performances",
    tags=["Student Performance APIs"],
)
api.include_router(extractions.router, prefix="/extractions", tags=["Extraction APIs"])
