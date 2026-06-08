from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class Practitioner(Base):
    __tablename__ = "practitioners"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(255), nullable=False)

    nik = Column(String(20))

    sip_number = Column(String(100))

    str_number = Column(String(100))

    specialization = Column(String(100))

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