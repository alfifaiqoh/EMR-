from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.core.dependencies import (
    get_current_user,
    require_doctor
)

from app.models.soap import SOAP
from app.models.diagnosis import Diagnosis
from app.models.treatment import Treatment

from app.schemas.encounter import (
    EncounterCreate,
    EncounterUpdate,
    EncounterResponse
)

from app.schemas.encounter_summary import (
    EncounterSummaryResponse
)

from app.crud.encounter import (
    create_encounter,
    get_encounters,
    get_encounter_by_id,
    update_encounter,
    delete_encounter
)

from app.crud.encounter_summary import (
    get_encounter_summary
)

router = APIRouter(
    prefix="/encounters",
    tags=["Encounters"],
    dependencies=[
        Depends(get_current_user)
    ]
)


# CREATE
@router.post(
    "/",
    response_model=EncounterResponse
)
def create_new_encounter(
    encounter: EncounterCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
):
    return create_encounter(
        db,
        encounter,
        int(current_user["sub"])
    )


# GET ALL
@router.get(
    "/",
    response_model=list[EncounterResponse]
)
def get_all_encounters(
    db: Session = Depends(get_db)
):
    return get_encounters(db)


# GET BY ID
@router.get(
    "/{encounter_id}",
    response_model=EncounterResponse
)
def get_single_encounter(
    encounter_id: int,
    db: Session = Depends(get_db)
):
    encounter = get_encounter_by_id(
        db,
        encounter_id
    )

    if not encounter:
        raise HTTPException(
            status_code=404,
            detail="Encounter not found"
        )

    return encounter


# GET SUMMARY
@router.get(
    "/{encounter_id}/summary",
    response_model=EncounterSummaryResponse
)
def get_summary(
    encounter_id: int,
    db: Session = Depends(get_db)
):
    summary = get_encounter_summary(
        db,
        encounter_id
    )

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Encounter not found"
        )

    return summary


# UPDATE
@router.put(
    "/{encounter_id}",
    response_model=EncounterResponse
)
def update_single_encounter(
    encounter_id: int,
    encounter: EncounterUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
):
    updated = update_encounter(
        db,
        encounter_id,
        encounter
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Encounter not found"
        )

    return updated


# START ENCOUNTER
@router.patch(
    "/{encounter_id}/start",
    response_model=EncounterResponse
)
def start_encounter(
    encounter_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
):
    encounter = get_encounter_by_id(
        db,
        encounter_id
    )

    if not encounter:
        raise HTTPException(
            status_code=404,
            detail="Encounter not found"
        )

    encounter.status = "IN_PROGRESS"

    db.commit()
    db.refresh(encounter)

    return encounter


# COMPLETE ENCOUNTER
@router.patch(
    "/{encounter_id}/complete",
    response_model=EncounterResponse
)
def complete_encounter(
    encounter_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
):
    encounter = get_encounter_by_id(
        db,
        encounter_id
    )

    if not encounter:
        raise HTTPException(
            status_code=404,
            detail="Encounter not found"
        )

    soap = (
        db.query(SOAP)
        .filter(
            SOAP.encounter_id == encounter_id
        )
        .first()
    )

    if not soap:
        raise HTTPException(
            status_code=400,
            detail="SOAP required"
        )

    diagnosis_count = (
        db.query(Diagnosis)
        .filter(
            Diagnosis.soap_id == soap.id
        )
        .count()
    )

    if diagnosis_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Diagnosis required"
        )

    treatment_count = (
        db.query(Treatment)
        .filter(
            Treatment.soap_id == soap.id
        )
        .count()
    )

    if treatment_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Treatment required"
        )

    encounter.status = "COMPLETED"

    db.commit()
    db.refresh(encounter)

    return encounter


# DELETE
@router.delete(
    "/{encounter_id}"
)
def delete_single_encounter(
    encounter_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
):
    deleted = delete_encounter(
        db,
        encounter_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Encounter not found"
        )

    return {
        "message": "Encounter deleted"
    }