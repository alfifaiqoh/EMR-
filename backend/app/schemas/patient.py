from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PatientCreate(BaseModel):
    nik: str
    full_name: str
    gender: str
    phone: Optional[str] = None


class PatientUpdate(BaseModel):
    nik: Optional[str] = None
    full_name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None


class PatientResponse(BaseModel):
    id: int
    nik: str
    full_name: str
    gender: str
    phone: Optional[str]
    ihs_number: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True