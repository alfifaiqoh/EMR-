from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("cis_patientsv2.id"),
        nullable=False
    )

    doctor_id = Column(
        Integer,
        nullable=True
    )

    chief_complaint = Column(
        String(255),
        nullable=True
    )

    status = Column(
        String(50),
        default="WAITING"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )