from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.base import Base
from sqlalchemy.orm import relationship

class Patient(Base):
    __tablename__ = "cis_patientsv2"

    id = Column(Integer, primary_key=True, index=True)
    nik = Column(String(20))
    fullname = Column(String(255))
    gender = Column(String(20))
    phone = Column(String(20))
    ihs_number = Column(String(100))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    encounters = relationship(
    "Encounter",
    back_populates="patient"
)