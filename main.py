from models import (UserBase, UserID, CreatePost,
                    Post, UserwithPost, UserUptade,
                    PostnoID, PostUpdate)

from operation import (crearusuario_db, show_user_db, find_one_user,
                       create_post, obtener_posts_db, Delete_user_db,
                       update_one_usuario_db, find_one_post, update_one_post_db,
                       Delete_post_db, show_ActiveUser_db, inactivo_Users_db, search_post_db)

from db import SessionDep, create_all_tables,  get_session
from sqlmodel import Session
from fastapi import FastAPI,HTTPException, UploadFile, File, Depends
from utils import save_img_local,save_img_remote



app = FastAPI(lifespan=create_all_tables)


@app.post("/CREATE_USERS",response_model=UserID)
async def cargarusuario(usuario:UserBase, session:SessionDep):
    return crearusuario_db(usuario, session)

@app.post("/CREATE_POST",response_model=Post)
def crear_post(post: CreatePost, session: Session = Depends(get_session)):
    result = create_post(post, session)
    if result is None:
        raise HTTPException(status_code=404, detail="user dont exist or user inactive")
    return result

@app.get("/SHOW_ALL_USERS",response_model=list[UserID])
async def mostrar_usuarios(session:SessionDep):
    return show_user_db(session)

@app.get("/SHOW_ALL_POSTS")
def ver_posts(session: Session = Depends(get_session)):
    return obtener_posts_db(session)

@app.get("/FIND_USER/{id}", response_model=UserwithPost)
async def show_one_user(id:int, session:SessionDep):
    user = find_one_user(id, session)
    if not (user):
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/FIND_POST/{id}", response_model=PostnoID)
async def get_one_post(id:int, session:SessionDep):
    post = find_one_post(id, session)
    if not (post):
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get("/User_active/")
async def get_all_UserActive(session:SessionDep):
    return show_ActiveUser_db(session)

@app.get("/User_inactive/")
async def get_all_UserInactive(session:SessionDep):
    return inactivo_Users_db(session)

@app.get("/Search_WithWord/")
async def search_with_word(word: str, session:SessionDep):
    return search_post_db(word, session)

@app.patch("/UPDATE_USER/{id}", response_model=UserBase)
async def update_user(id: int, usuario : UserUptade, session: SessionDep):
    update = update_one_usuario_db(id, usuario, session)
    if not (update):
        raise HTTPException(status_code=404, detail=f"{id} user not found")
    return update

@app.patch("/UPDATE_POST/{id}", response_model=PostnoID)
async def update_post(id: int, posteo : PostUpdate, session: SessionDep):
    update = update_one_post_db(id, posteo, session)
    if not (update):
        raise HTTPException(status_code=404, detail="Post not found")
    return update

@app.delete("/DELETE_USER/{id}", response_model=UserBase)
async def delete_user(id:int, session: SessionDep ):
    deleted  = Delete_user_db(id, session)
    if not (deleted):
        raise HTTPException(status_code=404, detail=f"{id} user not found")
    return deleted

@app.delete("/DELETE_POST/{id}", response_model=PostnoID)
async def delete_post(id: int, session: SessionDep):
    deleted = Delete_post_db(id, session)
    if not (deleted):
        raise HTTPException(status_code=404, detail=f"{id} post not found")
    return deleted

@app.post("/image/local")
async def image_save_local(img: UploadFile = File(...)):
    path = save_img_local(img)
    return {"path for your image": path}

@app.post("/image/remote")
async def image_save_remote(file:UploadFile = File(...)):
    url_img = save_img_remote(file)
    return {"url for your image":url_img}