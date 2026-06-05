from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    DateTime
)

from sqlalchemy.sql import func

from app.database.base import Base


class Treatment(Base):
    __tablename__ = "treatments"

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

    treatment_name = Column(
        String(255),
        nullable=False
    )

    price = Column(
        Numeric,
        nullable=True
    )

    notes = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )