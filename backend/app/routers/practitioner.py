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

from app.schemas.practitioner import (
    PractitionerCreate,
    PractitionerUpdate,
    PractitionerResponse
)

from app.crud.practitioner import (
    create_practitioner,
    get_practitioners,
    get_practitioner,
    update_practitioner,
    delete_practitioner
)

router = APIRouter(
    prefix="/practitioners",
    tags=["Practitioners"]
)


def practitioner_response(practitioner):
    return {
        "id": practitioner.id,
        "full_name": practitioner.full_name,
        "nik": practitioner.nik,
        "sip_number": practitioner.sip_number,
        "str_number": practitioner.str_number,
        "specialization": practitioner.specialization,
        "ihs_number": practitioner.ihs_number,
        "created_at": practitioner.created_at
    }


@router.post(
    "/",
    response_model=PractitionerResponse
)
def create_new_practitioner(
    practitioner: PractitionerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_practitioner = create_practitioner(
        db,
        practitioner
    )

    return practitioner_response(
        new_practitioner
    )


@router.get(
    "/",
    response_model=List[PractitionerResponse]
)
def get_all_practitioners(
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
    practitioners = get_practitioners(
        db,
        search,
        page,
        limit
    )

    return [
        practitioner_response(p)
        for p in practitioners
    ]


@router.get(
    "/{practitioner_id}",
    response_model=PractitionerResponse
)
def get_single_practitioner(
    practitioner_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    practitioner = get_practitioner(
        db,
        practitioner_id
    )

    if not practitioner:
        raise HTTPException(
            status_code=404,
            detail="Practitioner not found"
        )

    return practitioner_response(
        practitioner
    )


@router.put(
    "/{practitioner_id}",
    response_model=PractitionerResponse
)
def update_single_practitioner(
    practitioner_id: int,
    practitioner: PractitionerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated = update_practitioner(
        db,
        practitioner_id,
        practitioner
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Practitioner not found"
        )

    return practitioner_response(
        updated
    )


@router.delete(
    "/{practitioner_id}"
)
def delete_single_practitioner(
    practitioner_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = delete_practitioner(
        db,
        practitioner_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Practitioner not found"
        )

    return {
        "message": "Practitioner deleted successfully"
    }