from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_collection(db: Session, name: str, user: models.User):
    collection = models.Collection(name=name, owner=user)
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection


def get_collections(db: Session, user: models.User):
    return (
        db.query(models.Collection).filter(models.Collection.user_id == user.id).all()
    )


def get_collection(db: Session, collection_id: int, user: models.User):
    return (
        db.query(models.Collection)
        .filter(
            models.Collection.id == collection_id, models.Collection.user_id == user.id
        )
        .first()
    )


def add_todo(db: Session, title: str, collection: models.Collection):
    todo = models.Todo(title=title, collection=collection)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todos(db: Session, collection: models.Collection):
    return collection.todos
