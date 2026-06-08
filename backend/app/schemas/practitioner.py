from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PractitionerCreate(BaseModel):
    full_name: str = Field(
        ...,
        min_length=3,
        max_length=255
    )

    nik: Optional[str] = Field(
        None,
        min_length=16,
        max_length=16
    )

    sip_number: Optional[str] = Field(
        None,
        max_length=100
    )

    str_number: Optional[str] = Field(
        None,
        max_length=100
    )

    specialization: Optional[str] = Field(
        None,
        max_length=100
    )


class PractitionerUpdate(BaseModel):
    full_name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=255
    )

    nik: Optional[str] = Field(
        None,
        min_length=16,
        max_length=16
    )

    sip_number: Optional[str] = Field(
        None,
        max_length=100
    )

    str_number: Optional[str] = Field(
        None,
        max_length=100
    )

    specialization: Optional[str] = Field(
        None,
        max_length=100
    )


class PractitionerResponse(BaseModel):
    id: int
    full_name: str

    nik: Optional[str] = None
    sip_number: Optional[str] = None
    str_number: Optional[str] = None
    specialization: Optional[str] = None

    ihs_number: Optional[str] = None

    created_at: datetime

    class Config:
        from_attributes = True