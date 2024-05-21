from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp


class Mark(Timestamp, Base):
    """
    Represents a mark or score for a student in a particular subject.

    Attributes:
        mark_id (int): The unique identifier for the mark.
        stud_id (int): The student ID associated with the mark.
        student (Student): The student associated with the mark.
        subject_id (int): The subject ID associated with the mark.
        subject (Subject): The subject associated with the mark.
        section_id (int): The section ID associated with the mark.
        section (Section): The section associated with the mark.
        internal (int): The internal marks for the subject.
        external (int): The external marks for the subject.
        total (int): The total marks for the subject.
        result (Results): The result of the mark.
        grade (Grades): The grade of the mark.
    """

    __tablename__ = "marks"
    __table_args__ = (
        CheckConstraint("internal <= 50", name="check_internal"),
        CheckConstraint("external <= 50", name="check_external"),
        CheckConstraint("total <= 100", name="check_total"),
    )

    mark_id = Column(Integer, primary_key=True, index=True)
    stud_id = Column(
        Integer, ForeignKey("students.stud_id", ondelete="CASCADE"), nullable=False
    )
    student = relationship(
        "Student", back_populates="marks"
    )  # many-to-one relationship with Student
    subject_id = Column(
        Integer, ForeignKey("subjects.subject_id", ondelete="CASCADE"), nullable=False
    )
    subject = relationship(
        "Subject", back_populates="marks"
    )  # many-to-one relationship with Subject
    section_id = Column(
        Integer, ForeignKey("sections.section_id", ondelete="CASCADE"), nullable=False
    )
    section = relationship(
        "Section", back_populates="marks"
    )  # many-to-one relationship with Section
    internal = Column(Integer, index=True, nullable=False)
    external = Column(Integer, index=True, nullable=False)
    total = Column(Integer, index=True, nullable=False)
    result = Column(String(1), nullable=False)
    grade = Column(String(10), nullable=False)
