from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp


class ExtractionInvalid(Timestamp, Base):
    __tablename__ = "extraction_invalids"

    invalid_id = Column(Integer, primary_key=True, index=True)
    extraction_id = Column(
        Integer,
        ForeignKey("extractions.extraction_id", ondelete="CASCADE"),
        nullable=False,
    )
    extraction = relationship(
        "Extraction", back_populates="invalids"
    )  # many-to-one relationship with Extraction
    invalid_usns = Column(String, nullable=True)
    captcha_usns = Column(String, nullable=True)
    timeout_usns = Column(String, nullable=True)
