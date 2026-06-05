from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class PatientCreate(BaseModel):
    nik: str = Field(
        ...,
        min_length=16,
        max_length=16,
        description="NIK must be 16 digits"
    )

    full_name: str = Field(
        ...,
        min_length=3,
        max_length=255
    )

    gender: Literal["L", "P"]

    phone: Optional[str] = Field(
        None,
        min_length=10,
        max_length=15
    )


class PatientUpdate(BaseModel):
    nik: Optional[str] = Field(
        None,
        min_length=16,
        max_length=16
    )

    full_name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=255
    )

    gender: Optional[Literal["L", "P"]] = None

    phone: Optional[str] = Field(
        None,
        min_length=10,
        max_length=15
    )


class PatientResponse(BaseModel):
    id: int
    nik: str
    full_name: str
    gender: str
    phone: Optional[str] = None
    ihs_number: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True