from fastapi import FastAPI, HTTPException, Depends
from models import (usuariobase, identification, crearposteo, posteos, userconposts, UsuarioUpdate, posteosinid,
                    PostUpdate)
from operatio import (crearusuario_db, show_user_db, find_one_user, create_post, obtener_posts_db, Delete_user_db,
                      update_one_usuario_db, find_one_post, update_one_post_db, Delete_post_db)
from db import SessionDep, create_all_tables,  get_session
from sqlmodel import Session


app = FastAPI(lifespan=create_all_tables)


@app.post("/CREATE_USERS",response_model=identification)
async def cargarusuario(usuario:usuariobase, session:SessionDep):
    return crearusuario_db(usuario, session)

@app.post("/CREATE_POST",response_model=posteos)
def crear_post(post: crearposteo, session: Session = Depends(get_session)):
    return create_post(post, session)

@app.get("/SHOW_ALL_USERS",response_model=list[identification])
async def mostrar_usuarios(session:SessionDep):
    return show_user_db(session)

@app.get("/SHOW_ALL_POSTS")
def ver_posts(session: Session = Depends(get_session)):
    return obtener_posts_db(session)

@app.get("/FIND_USER/{id}", response_model=userconposts)
async def show_one_user(id:int, session:SessionDep):
    user = find_one_user(id, session)
    if not (user):
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/FIND_POST/{id}", response_model=posteosinid)
async def get_one_post(id:int, session:SessionDep):
    post = find_one_post(id, session)
    if not (post):
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.patch("/UPDATE_USER/{id}", response_model=usuariobase)
async def update_user(id: int, usuario : UsuarioUpdate, session: SessionDep):
    update = update_one_usuario_db(id, usuario, session)
    if not (update):
        raise HTTPException(status_code=404, detail=f"{id} user not found")
    return update

@app.patch("/UPDATE_POST/{id}", response_model=posteosinid)
async def update_post(id: int, posteo : PostUpdate, session: SessionDep):
    update = update_one_post_db(id, posteo, session)
    if not (update):
        raise HTTPException(status_code=404, detail="Post not found")
    return update

@app.delete("/DELETE_USER/{id}", response_model=usuariobase )
async def delete_user(id:int, session: SessionDep ):
    deleted  = Delete_user_db(id, session)
    if not (deleted):
        raise HTTPException(status_code=404, detail=f"{id} user not found")
    return deleted

@app.delete("/DELETE_POST/{id}", response_model=posteosinid)
async def delete_post(id: int, session: SessionDep):
    deleted = Delete_post_db(id, session)
    if not (deleted):
        raise HTTPException(status_code=404, detail=f"{id} post not found")
    return deleted
