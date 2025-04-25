from fastapi import APIRouter, Depends, HTTPException
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


@router.put("/collections/{collection_id}", response_model=schemas.CollectionInDB)
def update_collection(
    collection_id: int,
    name: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    collection = crud.get_collection(db, collection_id, current_user)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    collection.name = name
    db.commit()
    db.refresh(collection)
    return collection


@router.delete("/collections/{collection_id}")
def delete_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    collection = crud.get_collection(db, collection_id, current_user)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    db.delete(collection)
    db.commit()
    return {"msg": "Collection deleted successfully"}
