from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class SOAP(Base):
    __tablename__ = "soap_notes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    encounter_id = Column(
        Integer,
        ForeignKey("encounters.id"),
        nullable=False
    )

    subjective = Column(
        Text,
        nullable=True
    )

    objective = Column(
        Text,
        nullable=True
    )

    assessment = Column(
        Text,
        nullable=True
    )

    plan = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    encounter = relationship(
    "Encounter",
    back_populates="soaps"
    )

    diagnoses = relationship(
    "Diagnosis",
    back_populates="soap"
    )

    treatments = relationship(
    "Treatment",
    back_populates="soap"
    )