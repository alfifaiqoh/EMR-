from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.database.base import Base


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    soap_id = Column(
        Integer,
        ForeignKey("soap_notes.id"),
        nullable=False
    )

    diagnosis_name = Column(
        String(255),
        nullable=False
    )

    icd_code = Column(
        String(50),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )