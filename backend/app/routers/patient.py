from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)
from sqlalchemy.orm import Session
from typing import List

from app.database.dependencies import get_db
from app.core.dependencies import get_current_user

from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse
)

from app.schemas.history import (
    PatientHistoryResponse
)

from app.crud.patient import (
    create_patient,
    get_patients,
    get_patient,
    update_patient,
    delete_patient,
    get_patient_history
)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


def patient_response(patient):
    return {
        "id": patient.id,
        "nik": patient.nik,
        "full_name": patient.full_name,
        "gender": patient.gender,
        "phone": patient.phone,
        "ihs_number": patient.ihs_number,
        "created_at": patient.created_at
    }


# CREATE
@router.post(
    "/",
    response_model=PatientResponse
)
def create_new_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_patient = create_patient(
        db,
        patient
    )

    if not new_patient:
        raise HTTPException(
            status_code=400,
            detail="NIK already registered"
        )

    return patient_response(
        new_patient
    )


# GET ALL + SEARCH + PAGINATION
@router.get(
    "/",
    response_model=List[PatientResponse]
)
def get_all_patients(
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(
        10,
        ge=1,
        le=100
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    patients = get_patients(
        db,
        search,
        page,
        limit
    )

    return [
        patient_response(patient)
        for patient in patients
    ]


# GET HISTORY
@router.get(
    "/{patient_id}/history",
    response_model=PatientHistoryResponse
)
def get_history(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    patient = get_patient_history(
        db,
        patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


# GET BY ID
@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_single_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    patient = get_patient(
        db,
        patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient_response(
        patient
    )


# UPDATE
@router.put(
    "/{patient_id}",
    response_model=PatientResponse
)
def update_single_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated = update_patient(
        db,
        patient_id,
        patient
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient_response(
        updated
    )


# DELETE
@router.delete(
    "/{patient_id}"
)
def delete_single_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = delete_patient(
        db,
        patient_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return {
        "message": "Patient deleted successfully"
    }