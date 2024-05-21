from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp


class StudentPerformance(Timestamp, Base):
    __tablename__ = "student_performances"

    stud_perf_id = Column(Integer, primary_key=True, index=True)
    stud_id = Column(
        Integer, ForeignKey("students.stud_id", ondelete="CASCADE"), nullable=False
    )
    # many to one relationship with Students
    student = relationship("Student", back_populates="student_performances")
    sem_id = Column(
        Integer, ForeignKey("semesters.sem_id", ondelete="CASCADE"), nullable=False
    )
    # many to one relationship with Semesters
    semester = relationship("Semester", back_populates="student_performances")
    total = Column(Integer, index=True, nullable=False)
    percentage = Column(Numeric(5, 2), index=True, nullable=False)
    sgpa = Column(Numeric(3, 1), index=True, nullable=False)
