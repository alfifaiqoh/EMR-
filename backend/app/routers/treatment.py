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

from app.schemas.treatment import (
    TreatmentCreate,
    TreatmentUpdate,
    TreatmentResponse
)

from app.crud.treatment import (
    create_treatment,
    get_treatments,
    get_treatment_by_id,
    update_treatment,
    delete_treatment
)

router = APIRouter(
    prefix="/treatments",
    tags=["Treatments"]
)


@router.post(
    "/",
    response_model=TreatmentResponse
)
def create_new_treatment(
    treatment: TreatmentCreate,
    db: Session = Depends(get_db)
):
    return create_treatment(
        db,
        treatment
    )
Depends(require_doctor)

@router.get(
    "/",
    response_model=list[TreatmentResponse]
)
def get_all_treatments(
    db: Session = Depends(get_db)
):
    return get_treatments(db)
Depends(require_doctor)

@router.get(
    "/{treatment_id}",
    response_model=TreatmentResponse
)
def get_single_treatment(
    treatment_id: int,
    db: Session = Depends(get_db)
):
    treatment = get_treatment_by_id(
        db,
        treatment_id
    )

    if not treatment:
        raise HTTPException(
            status_code=404,
            detail="Treatment not found"
        )

    return treatment
Depends(require_doctor)

@router.put(
    "/{treatment_id}",
    response_model=TreatmentResponse
)
def update_single_treatment(
    treatment_id: int,
    treatment: TreatmentUpdate,
    db: Session = Depends(get_db)
):
    updated = update_treatment(
        db,
        treatment_id,
        treatment
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Treatment not found"
        )

    return updated
Depends(require_doctor)

@router.delete(
    "/{treatment_id}"
)
def delete_single_treatment(
    treatment_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_treatment(
        db,
        treatment_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Treatment not found"
        )

    return {
        "message":
        "Treatment deleted"
    }
Depends(require_doctor)