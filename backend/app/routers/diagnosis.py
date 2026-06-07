from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from app.core.dependencies import (
    require_doctor
)
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.diagnosis import (
    DiagnosisCreate,
    DiagnosisUpdate,
    DiagnosisResponse
)

from app.crud.diagnosis import (
    create_diagnosis,
    get_diagnoses,
    get_diagnosis_by_id,
    update_diagnosis,
    delete_diagnosis
)

router = APIRouter(
    prefix="/diagnoses",
    tags=["Diagnoses"]
)


@router.post(
    "/",
    response_model=DiagnosisResponse
)
def create_new_diagnosis(
    diagnosis: DiagnosisCreate,
    db: Session = Depends(get_db)
):
    return create_diagnosis(
        db,
        diagnosis
    )
Depends(require_doctor)


@router.get(
    "/",
    response_model=list[DiagnosisResponse]
)
def get_all_diagnoses(
    db: Session = Depends(get_db)
):
    return get_diagnoses(db)
Depends(require_doctor)

@router.get(
    "/{diagnosis_id}",
    response_model=DiagnosisResponse
)
def get_single_diagnosis(
    diagnosis_id: int,
    db: Session = Depends(get_db)
):
    diagnosis = get_diagnosis_by_id(
        db,
        diagnosis_id
    )

    if not diagnosis:
        raise HTTPException(
            status_code=404,
            detail="Diagnosis not found"
        )

    return diagnosis
Depends(require_doctor)

@router.put(
    "/{diagnosis_id}",
    response_model=DiagnosisResponse
)
def update_single_diagnosis(
    diagnosis_id: int,
    diagnosis: DiagnosisUpdate,
    db: Session = Depends(get_db)
):
    updated = update_diagnosis(
        db,
        diagnosis_id,
        diagnosis
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Diagnosis not found"
        )

    return updated
Depends(require_doctor)

@router.delete(
    "/{diagnosis_id}"
)
def delete_single_diagnosis(
    diagnosis_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_diagnosis(
        db,
        diagnosis_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Diagnosis not found"
        )

    return {
        "message":
        "Diagnosis deleted"
    }
Depends(require_doctor)