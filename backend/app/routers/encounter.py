from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.dependencies import (
    get_db
)

from app.core.dependencies import (
    get_current_user,
    require_doctor
)
from app.schemas.encounter import (
    EncounterCreate,
    EncounterUpdate,
    EncounterResponse
)

from app.crud.encounter import (
    create_encounter,
    get_encounters,
    get_encounter_by_id,
    update_encounter,
    delete_encounter
)

router = APIRouter(
    prefix="/encounters",
    tags=["Encounters"]
)


@router.post(
    "/",
    response_model=EncounterResponse
)
def create_new_encounter(
    encounter: EncounterCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
    require_doctor
    )
):

    new_encounter = (
        create_encounter(
            db,
            encounter,
            int(
                current_user["sub"]
            )
        )
    )

    return new_encounter

@router.get(
    "/",
    response_model=list[EncounterResponse]
)
def get_all_encounters(
    db: Session = Depends(get_db)
):
    return get_encounters(db)


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


@router.put(
    "/{encounter_id}",
    response_model=EncounterResponse
)
def update_single_encounter(
    encounter_id: int,
    encounter: EncounterUpdate,
    db: Session = Depends(get_db)
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


@router.delete(
    "/{encounter_id}"
)
def delete_single_encounter(
    encounter_id: int,
    db: Session = Depends(get_db)
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
        "message":
        "Encounter deleted"
    }