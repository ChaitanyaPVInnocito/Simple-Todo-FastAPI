import re
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, schemas
from app.auth_utils import create_access_token, get_db
from email_validator import validate_email, EmailNotValidError


router = APIRouter(tags=["auth"])


@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        validate_email(user.username)
    except EmailNotValidError:
        raise HTTPException(
            status_code=400, detail="Username must be a valid email address"
        )   

    password = user.password
    username = user.username.lower()

    if len(password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters long"
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one lowercase letter",
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase letter",
        )
    if not re.search(r"[0-9]", password):
        raise HTTPException(
            status_code=400, detail="Password must contain at least one number"
        )
    if not re.search(r'[!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~]', password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one special character",
        )
    if password[0].isdigit() or password[-1].isdigit():
        raise HTTPException(
            status_code=400, detail="Password must not start or end with a number"
        )
    if password.lower() == username or password.lower() == username[::-1]:
        raise HTTPException(
            status_code=400,
            detail="Password must not be the same as the username or its reverse",
        )

    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    crud.create_user(db, user)
    return {"msg": "User created successfully"}


@router.post("/token", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
