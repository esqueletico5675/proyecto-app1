from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    name: str = Field(default=None, min_length=1, max_length=15)
    pin: int
    image_url: Optional[str] = Field(default=None)

class UserID(UserBase, table=True):
    id: int = Field(primary_key=True, default=None)
    activo: bool = Field(default=True)
    posts: list["Post"] = Relationship(back_populates="usuario")

class Post(SQLModel, table=True):
    contador_post: Optional[int] = Field(default=None, primary_key=True)
    contenido: str = Field(default=None)
    id_usuario: int = Field(default=None, foreign_key="userid.id")
    pin: Optional[int] = Field(default=0)
    likes_count: Optional[int] = Field(default=0)
    image_url: Optional[str] = Field(default=None)
    usuario: Optional[UserID] = Relationship(back_populates="posts")

class CreatePost(SQLModel):
    contenido: str
    id_usuario: int
    image_url: Optional[str] = Field(default=None)

class PostnoID(SQLModel):
    contenido: str
    id_usuario: int
    contador_post: int

class UserwithPost(SQLModel):
    id: int
    name: str
    posts: list[PostnoID] = []

class UserUptade(SQLModel):
    name: str | None = None
    image_url: str | None = None

class PostUpdate(SQLModel):
    contenido: str | None = None
