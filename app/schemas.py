from pydantic import BaseModel
from typing import List, Optional


class TodoBase(BaseModel):
    title: str


class TodoCreate(TodoBase):
    pass


class TodoInDB(TodoBase):
    id: int

    class Config:
        orm_mode = True


class CollectionBase(BaseModel):
    name: str


class CollectionCreate(CollectionBase):
    pass


class CollectionInDB(CollectionBase):
    id: int
    todos: List[TodoInDB] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
