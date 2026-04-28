from sqlalchemy import true
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from models import usuariobase,identification, posteos, crearposteo, UsuarioUpdate, PostUpdate

def crearusuario_db(usuario:usuariobase,session:Session):
    new_usuario = identification.model_validate(usuario)
    session.add(new_usuario)
    session.commit()
    session.refresh(new_usuario)
    return new_usuario

def show_user_db(session:Session):
    return session.exec(select(identification)).all()

def find_one_user (id: int ,session:Session):
    try:
        user = session.get_one(identification, id)
        if not user.activo:
            return None
        return user
    except NoResultFound:
        return None

def find_one_post (id: int ,session:Session):
    try:
        return session.get_one(posteos, id)
    except NoResultFound:
        return None

def create_post(post:crearposteo, session:Session):
    user = find_one_user(post.id_usuario, session)
    if user is None:
        return None
    nuevopost = posteos.model_validate(post)
    session.add(nuevopost)
    session.commit()
    session.refresh(nuevopost)
    return nuevopost

def obtener_posts_db(session: Session):
    posts = session.exec(select(posteos)).all()
    return [{"Contenido": p.contenido, "ID_usuario": p.id_usuario, "#Contador_post":p.contador_post} for p in posts]

def Delete_user_db(id: int, session: Session):
    try:
        user = session.get_one(identification, id)
        user.activo = False
        session.add(user)
        session.commit()
        session.refresh(user)
    except NoResultFound:
        return None
    except NoResultFound:
        return None

def Delete_post_db(id: int, session: Session):
    try:
        post = session.get_one(posteos, id)
        session.delete(post)
        session.commit()
        return post
    except NoResultFound:
        return None

def update_one_usuario_db(id: int, new_usuario: UsuarioUpdate, session: Session):
    usuario=find_one_user(id, session)
    if usuario is None:
        return None
    usuario_update= new_usuario.model_dump(exclude_unset=True)
    usuario.sqlmodel_update(usuario_update)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

def update_one_post_db(id: int, new_post: PostUpdate, session : Session):
    posteo = find_one_post(id, session)
    if posteo is None:
        return None
    posteo_update = new_post.model_dump(exclude_unset=True)
    posteo.sqlmodel_update(posteo_update)
    session.add(posteo)
    session.commit()
    session.refresh(posteo)
    return posteo

def search_post_db (keyword: str, session: Session):
    return session.exec(select(posteos).where(posteos.contenido.contains(keyword))).all()

def show_ActiveUser_db(session: Session):
    return  session.exec(select(identification).where(identification.activo == True)).all()

def inactivo_Users_db( session: Session):
    return session.exec(select(identification).where(identification.activo == False)).all()
