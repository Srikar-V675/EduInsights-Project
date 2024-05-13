from fastapi import FastAPI

from api import batches, departments, sections, semesters

api = FastAPI(
    title="EduInsights API",
    description="API for managing VTU results, analysis and extraction.",
    version="0.1.0",
)

api.include_router(departments.router, prefix="/departments", tags=["Department APIs"])
api.include_router(batches.router, prefix="/batches", tags=["Batch APIs"])
api.include_router(semesters.router, prefix="/semesters", tags=["Semester APIs"])
api.include_router(sections.router, prefix="/sections", tags=["Section APIs"])
