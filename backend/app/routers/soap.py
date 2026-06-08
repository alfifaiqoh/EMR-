from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.soap import (
    SOAPCreate,
    SOAPUpdate,
    SOAPResponse
)

from app.core.dependencies import (
    require_doctor
)

from app.crud.soap import (
    create_soap,
    get_soaps,
    get_soap_by_id,
    update_soap,
    delete_soap
)

router = APIRouter(
    prefix="/soap",
    tags=["SOAP"]
)


# CREATE
@router.post(
    "/",
    response_model=SOAPResponse
)
def create_new_soap(
    soap: SOAPCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
):
    return create_soap(
        db,
        soap
    )


# GET ALL
@router.get(
    "/",
    response_model=list[SOAPResponse]
)
def get_all_soaps(
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
):
    return get_soaps(db)


# GET BY ID
@router.get(
    "/{soap_id}",
    response_model=SOAPResponse
)
def get_single_soap(
    soap_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
):
    soap = get_soap_by_id(
        db,
        soap_id
    )

    if not soap:
        raise HTTPException(
            status_code=404,
            detail="SOAP not found"
        )

    return soap


# UPDATE
@router.put(
    "/{soap_id}",
    response_model=SOAPResponse
)
def update_single_soap(
    soap_id: int,
    soap: SOAPUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
):
    updated = update_soap(
        db,
        soap_id,
        soap
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="SOAP not found"
        )

    return updated


# DELETE
@router.delete(
    "/{soap_id}"
)
def delete_single_soap(
    soap_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_doctor)
):
    deleted = delete_soap(
        db,
        soap_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="SOAP not found"
        )

    return {
        "message": "SOAP deleted successfully"
    }