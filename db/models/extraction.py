from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp


class Extraction(Timestamp, Base):
    __tablename__ = "extractions"

    extraction_id = Column(Integer, primary_key=True, index=True)
    section_id = Column(
        Integer, ForeignKey("sections.section_id", ondelete="CASCADE"), nullable=False
    )
    section = relationship(
        "Section", back_populates="extractions"
    )  # many-to-one relationship with Section
    sem_id = Column(
        Integer, ForeignKey("semesters.sem_id", ondelete="CASCADE"), nullable=False
    )
    semester = relationship(
        "Semester", back_populates="extractions"
    )  # many-to-one relationship with Semester
    total_usns = Column(Integer, index=True, nullable=False)
    num_completed = Column(Integer, index=True, default=0, nullable=False)
    num_invalid = Column(Integer, index=True, default=0, nullable=False)
    reattempts = Column(Integer, index=True, default=0, nullable=False)
    progress = Column(Numeric(5, 2), index=True, default=0.0, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    failed = Column(Boolean, default=False, nullable=False)
    time_taken = Column(Numeric(7, 2), index=True, default=0.0, nullable=False)
