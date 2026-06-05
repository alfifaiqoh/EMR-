from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database.dependencies import get_db
from app.models.patient import Patient
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse
)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


# CREATE
@router.post(
    "/",
    response_model=PatientResponse
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    existing_patient = (
        db.query(Patient)
        .filter(Patient.nik == patient.nik)
        .first()
    )

    if existing_patient:
        raise HTTPException(
            status_code=400,
            detail="NIK already registered"
        )

    new_patient = Patient(
        nik=patient.nik,
        fullname=patient.full_name,
        gender=patient.gender,
        phone=patient.phone
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return {
        "id": new_patient.id,
        "nik": new_patient.nik,
        "full_name": new_patient.fullname,
        "gender": new_patient.gender,
        "phone": new_patient.phone,
        "ihs_number": new_patient.ihs_number,
        "created_at": new_patient.created_at
    }


# GET ALL + SEARCH + PAGINATION
@router.get(
    "/",
    response_model=List[PatientResponse]
)
def get_patients(
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Patient)

    if search:
        query = query.filter(
            (Patient.fullname.ilike(f"%{search}%")) |
            (Patient.nik.ilike(f"%{search}%"))
        )

    skip = (page - 1) * limit

    patients = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = []

    for patient in patients:
        result.append({
            "id": patient.id,
            "nik": patient.nik,
            "full_name": patient.fullname,
            "gender": patient.gender,
            "phone": patient.phone,
            "ihs_number": patient.ihs_number,
            "created_at": patient.created_at
        })

    return result


# GET BY ID
@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return {
        "id": patient.id,
        "nik": patient.nik,
        "full_name": patient.fullname,
        "gender": patient.gender,
        "phone": patient.phone,
        "ihs_number": patient.ihs_number,
        "created_at": patient.created_at
    }


# UPDATE
@router.put(
    "/{patient_id}",
    response_model=PatientResponse
)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db)
):
    db_patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not db_patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if patient.nik:
        db_patient.nik = patient.nik

    if patient.full_name:
        db_patient.fullname = patient.full_name

    if patient.gender:
        db_patient.gender = patient.gender

    if patient.phone:
        db_patient.phone = patient.phone

    db.commit()
    db.refresh(db_patient)

    return {
        "id": db_patient.id,
        "nik": db_patient.nik,
        "full_name": db_patient.fullname,
        "gender": db_patient.gender,
        "phone": db_patient.phone,
        "ihs_number": db_patient.ihs_number,
        "created_at": db_patient.created_at
    }


# DELETE
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)
    db.commit()

    return {
        "message": "Patient deleted successfully"
    }