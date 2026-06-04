from starlette.responses import HTMLResponse

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
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form



app = FastAPI(lifespan=create_all_tables)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home (request: Request):
    return templates.TemplateResponse({"request": request} ,"index.html", context={})

@app.get ("/usuarios")
def ver_users (request:Request, session:SessionDep):
    usuarios = show_user_db(session)
    return templates.TemplateResponse( request = request, name = "usuarios.html",context = {"usuarios": usuarios})

@app.get ("/usuarios/{id}")
async def user_Details (id:int,request:Request, session:SessionDep):
    user = find_one_user(id, session)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return templates.TemplateResponse( request = request, name = "user_details.html",context = {"usuario": user})

@app.get("/posts")
def ver_posts(request: Request, session: SessionDep):
    posts = obtener_posts_db(session)
    return templates.TemplateResponse(request=request, name="posts.html", context={"posts": posts})

@app.get("/buscar")
def buscar_posts(request: Request, word: str, session: SessionDep):
        posts = search_post_db(word, session)
        return templates.TemplateResponse(request=request, name="posts.html", context={"posts": posts, "word": word})

@app.post("/form/crear-usuario", response_class=HTMLResponse)
async def form_crear_usuario(
    request: Request,
    session: SessionDep,
    name: str = Form(),
    pin: int = Form(),
    imagen: UploadFile = File(default=None),
):
    image_url = None
    if imagen and imagen.filename:
        image_url = save_img_remote(imagen)
    usuario = UserBase(name=name, pin=pin, image_url=image_url)
    resultado = crearusuario_db(usuario, session)
    return templates.TemplateResponse(
        request=request,
        name="usuario_creado.html",
        context={"usuario": resultado})

@app.post("/form/crear-post", response_class=HTMLResponse)
async def form_crear_post(
    request: Request,
    session: SessionDep,
    user_id: int = Form(),
    contenido: str = Form(),
    imagen: UploadFile = File(default=None),
):
    image_url = None
    if imagen and imagen.filename:
        image_url = save_img_remote(imagen)
    post = CreatePost(id_usuario=user_id, contenido=contenido, image_url=image_url)
    resultado = create_post(post, session)
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no existe o está inactivo")
    return templates.TemplateResponse(
        request=request,
        name="post_creado.html",
        context={"post": resultado}
    )

@app.get("/posts/{id}/editar", response_class=HTMLResponse)
async def form_editar_post(id: int, request: Request, session: SessionDep):
    post = find_one_post(id, session)
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return templates.TemplateResponse(
        request=request,
        name="editar_post.html",
        context={"post": post}
    )

@app.post("/posts/{id}/editar", response_class=HTMLResponse)
async def actualizar_post_form(
    id: int,
    request: Request,
    session: SessionDep,
    pin: int = Form(),
    contenido: str = Form(),
    imagen: UploadFile = File(default=None),
):
    post = find_one_post(id, session)
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    if post.pin != pin:
        return templates.TemplateResponse(
            request=request,
            name="editar_post.html",
            context={"post": post, "error": "PIN incorrecto ❌"}
        )
    image_url = post.image_url
    if imagen and imagen.filename and imagen.size > 0:
        image_url = save_img_remote(imagen)
    update = update_one_post_db(id, PostUpdate(contenido=contenido), session)
    update.image_url = image_url
    session.add(update)
    session.commit()
    session.refresh(update)
    return templates.TemplateResponse(
        request=request,
        name="post_creado.html",
        context={"post": update}
    )

@app.post("/posts/{id}/borrar", response_class=HTMLResponse)
async def borrar_post_form(
    id: int,
    request: Request,
    session: SessionDep,
    pin: int = Form(),
):
    post = find_one_post(id, session)
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    if post.pin != pin:
        return templates.TemplateResponse(
            request=request,
            name="editar_post.html",
            context={"post": post, "error": "PIN incorrecto ❌"}
        )
    Delete_post_db(id, session)
    return templates.TemplateResponse(
        request=request,
        name="post_borrado.html",
        context={}
    )

@app.get("/usuarios/{id}/editar", response_class=HTMLResponse)
async def form_editar_usuario(id: int, request: Request, session: SessionDep):
    usuario = find_one_user(id, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return templates.TemplateResponse(
        request=request,
        name="editar_usuario.html",
        context={"usuario": usuario}
    )

@app.post("/usuarios/{id}/editar", response_class=HTMLResponse)
async def actualizar_usuario_form(
    id: int,
    request: Request,
    session: SessionDep,
    pin: int = Form(),
    name: str = Form(),
    imagen: UploadFile = File(default=None),
):
    usuario = find_one_user(id, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.pin != pin:
        return templates.TemplateResponse(
            request=request,
            name="editar_usuario.html",
            context={"usuario": usuario, "error": "PIN incorrecto ❌"}
        )
    image_url = usuario.image_url
    if imagen and imagen.filename and imagen.size > 0:
        image_url = save_img_remote(imagen)
    update = update_one_usuario_db(id, UserUptade(name=name), session)
    update.image_url = image_url
    session.add(update)
    session.commit()
    session.refresh(update)
    return templates.TemplateResponse(
        request=request,
        name="usuario_creado.html",
        context={"usuario": update}
    )

@app.post("/form/borrar-usuario/{id}", response_class=HTMLResponse)
async def borrar_usuario_form(
    id: int,
    request: Request,
    session: SessionDep,
    pin: int = Form(),
):
    usuario = find_one_user(id, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.pin != pin:
        return templates.TemplateResponse(
            request=request,
            name="editar_usuario.html",
            context={"usuario": usuario, "error": "PIN incorrecto ❌"}
        )
    Delete_user_db(id, session)
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/usuarios", status_code=303)

@app.post("/posts/{id}/like", response_class=HTMLResponse)
async def dar_like(id: int, request: Request, session: SessionDep):
    post = find_one_post(id, session)
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    post.likes_count = (post.likes_count or 0) + 1
    session.add(post)
    session.commit()
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/posts", status_code=303)

@app.post("/posts/{id}/quitar-like", response_class=HTMLResponse)
async def quitar_like(id: int, request: Request, session: SessionDep):
    post = find_one_post(id, session)
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    post.likes_count = max(0, (post.likes_count or 0) - 1)
    session.add(post)
    session.commit()
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/posts", status_code=303)

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