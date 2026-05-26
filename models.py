from typing import Optional

from sqlalchemy import true
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    name:str = Field(default=None,
                     min_length=1,
                    max_length=15)

class UserID(UserBase, table=True):
    id: int = Field(primary_key=True, default=None)
    activo: bool = Field(default=True)
    posts: list["Post"] = Relationship(back_populates="usuario")

class Post(SQLModel, table=True):
    contador_post: Optional[int] = Field(default=None, primary_key=True)
    contenido: str = Field(default=None)
    id_usuario: int = Field(default=None, foreign_key="userid.id")
    usuario: Optional[UserID] = Relationship(back_populates="posts")

class CreatePost(SQLModel):
    contenido:str
    id_usuario:int

class PostnoID(SQLModel):
    contenido: str
    id_usuario: int
    contador_post: int

class UserwithPost(SQLModel):
    id: int
    name: str
    posts: list[PostnoID] = []

class UserUptade(UserBase):
    name: str | None = None

class PostUpdate(SQLModel):
    contenido: str | None = None
