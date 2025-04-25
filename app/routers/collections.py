from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.auth_utils import get_current_user, get_db

router = APIRouter()


@router.post("/collections", response_model=schemas.CollectionInDB)
def create(
    name: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return crud.create_collection(db, name, current_user)


@router.get("/collections", response_model=list[schemas.CollectionInDB])
def list_collections(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return crud.get_collections(db, current_user)
