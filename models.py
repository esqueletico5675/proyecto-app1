from typing import Optional

from sqlalchemy import true
from sqlmodel import SQLModel, Field, Relationship


class usuariobase(SQLModel):
    name:str = Field(default=None,
                     min_length=1,
                    max_length=15)

class identification(usuariobase, table=True):
    id:int = Field(primary_key=True, default=None)
    posts: list["posteos"] = Relationship(back_populates="usuario")

class posteos(SQLModel, table=True):
    contador_post: Optional[int] = Field(default=None, primary_key=True)
    contenido:str = Field(default=None)
    id_usuario: int = Field(default=None, foreign_key="identification.id")
    usuario: Optional[identification]   = Relationship(back_populates="posts")

class crearposteo(SQLModel):
    contenido:str
    id_usuario:int

class posteosinid(SQLModel):
    contenido: str
    id_usuario: int
    contador_post: int

class userconposts(SQLModel):
    id: int
    name: str
    posts: list[posteosinid] = []

class UserUpdate(usuariobase):
    name: str | None = Field(None,exclude=True)