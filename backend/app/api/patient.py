from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.patient import Patient
from app.schemas.patient import (
    PatientCreate,
    PatientResponse
)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post(
    "/",
    response_model=PatientResponse
)
def create_patient(
    payload: PatientCreate,
    db: Session = Depends(get_db)
):

    patient = Patient(
        nik=payload.nik,
        fullname=payload.fullname,
        gender=payload.gender
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient