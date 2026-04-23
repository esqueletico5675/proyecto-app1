from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from models import usuariobase,identification, posteos, crearposteo

def crearusuario_db(usuario:usuariobase,session:Session):
    new_usuario = identification.model_validate(usuario)
    session.add(new_usuario)
    session.commit()
    session.refresh(new_usuario)
    return new_usuario

def show_user_db(session:Session):
    return session.exec(select(identification))

def find_one_user (id: int ,session:Session):
    try:
        return session.get_one(identification,id)
    except NoResultFound:
        return None

def create_post(post:crearposteo, session:Session):
    nuevopost = posteos.from_orm(post)
    session.add(nuevopost)
    session.commit()
    session.refresh(nuevopost)
    return nuevopost

def obtener_posts_db(session: Session):
    posts = session.exec(select(posteos)).all()
    return [{"contenido": p.contenido, "id_usuario": p.id_usuario} for p in posts]


def Delete_user_db(id: int, session: Session):
    try:
        user = session.get_one(identification, id)
        for post in user.posts:
            session.delete(post)
        session.delete(user)
        session.commit()
        return user
    except NoResultFound:
        return None