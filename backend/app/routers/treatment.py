from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.core.dependencies import (
    require_doctor
)

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


# CREATE
@router.post(
    "/",
    response_model=TreatmentResponse
)
def create_new_treatment(
    treatment: TreatmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
):
    return create_treatment(
        db,
        treatment
    )


# GET ALL
@router.get(
    "/",
    response_model=list[TreatmentResponse]
)
def get_all_treatments(
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
):
    return get_treatments(db)


# GET BY ID
@router.get(
    "/{treatment_id}",
    response_model=TreatmentResponse
)
def get_single_treatment(
    treatment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
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


# UPDATE
@router.put(
    "/{treatment_id}",
    response_model=TreatmentResponse
)
def update_single_treatment(
    treatment_id: int,
    treatment: TreatmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
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


# DELETE
@router.delete(
    "/{treatment_id}"
)
def delete_single_treatment(
    treatment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
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
        "message": "Treatment deleted"
    }