from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp


class Subject(Timestamp, Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True, index=True)
    sub_code = Column(String(10), index=True, nullable=False)
    sem_id = Column(Integer, ForeignKey("semesters.sem_id"), nullable=False)
    # many - one relationship -> semester
    semester = relationship("Semester", back_populates="subjects")
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False)
    # many-one relationship -> batch
    batch = relationship("Batch", back_populates="subjects")
    sub_name = Column(String(70), index=True, nullable=False)
    # avg_marks, num_pass,... -> add more as needed.

    # one-many relationship -> marks
    marks = relationship("Mark", back_populates="subject")
