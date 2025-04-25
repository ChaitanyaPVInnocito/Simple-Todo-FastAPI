from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.auth_utils import get_current_user, get_db

router = APIRouter()


@router.post("/collections/{collection_id}/todos", response_model=schemas.TodoInDB)
def add_todo(
    collection_id: int,
    title: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    collection = crud.get_collection(db, collection_id, current_user)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return crud.add_todo(db, title, collection)


@router.get("/collections/{collection_id}/todos", response_model=list[schemas.TodoInDB])
def list_todos(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    collection = crud.get_collection(db, collection_id, current_user)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return crud.get_todos(db, collection)


@router.put("/todos/{todo_id}", response_model=schemas.TodoInDB)
def update_todo(
    todo_id: int,
    todo: schemas.TodoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    updated = crud.update_todo(db, todo_id, todo.title, current_user)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found or unauthorized")
    return updated


@router.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    deleted = crud.delete_todo(db, todo_id, current_user)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found or unauthorized")
    return {"msg": "Todo deleted successfully"}
