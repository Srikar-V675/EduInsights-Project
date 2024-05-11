from fastapi import FastAPI

from api import batches, departments

api = FastAPI(
    title="EduInsights API",
    description="API for managing VTU results and extraction.",
    version="0.1.0",
)

api.include_router(departments.router, prefix="/departments", tags=["Department APIs"])
api.include_router(batches.router, prefix="/batches", tags=["Batch APIs"])
