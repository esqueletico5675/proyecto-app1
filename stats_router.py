"""
stats_router.py — Criterio 15
Router de estadísticas/dashboard para la app FastAPI.
Registrar en main.py con: app.include_router(stats_router)
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select, func
from db import get_session, SessionDep
from models import UserID, Post

# Router dedicado a estadísticas
stats_router = APIRouter(prefix="/stats", tags=["Estadísticas"])

templates = Jinja2Templates(directory="templates")


def get_dashboard_data(session: Session) -> dict:
    """
    Calcula y retorna todas las métricas del dashboard.
    Devuelve un dict listo para pasarle al template o como JSON.
    """

    # --- Totales generales ---
    total_posts = session.exec(select(func.count(Post.contador_post))).one()
    total_users = session.exec(select(func.count(UserID.id))).one()
    active_users = session.exec(
        select(func.count(UserID.id)).where(UserID.activo == True)
    ).one()
    inactive_users = total_users - active_users

    # Total de likes acumulados en todos los posts
    total_likes = session.exec(select(func.sum(Post.likes_count))).one() or 0

    # --- Top 5 posts con más likes ---
    top_posts = session.exec(
        select(Post).order_by(Post.likes_count.desc()).limit(5)
    ).all()

    # --- Top 5 usuarios por cantidad de posts publicados ---
    # Agrupa posts por id_usuario y cuenta cuántos tiene cada uno
    top_users_by_posts_raw = session.exec(
        select(UserID.id, UserID.name, func.count(Post.contador_post).label("post_count"))
        .join(Post, Post.id_usuario == UserID.id, isouter=True)
        .group_by(UserID.id)
        .order_by(func.count(Post.contador_post).desc())
        .limit(5)
    ).all()

    top_users_by_posts = [
        {"id": row[0], "name": row[1], "post_count": row[2]}
        for row in top_users_by_posts_raw
    ]

    # --- Top 5 usuarios por likes totales recibidos en sus posts ---
    top_users_by_likes_raw = session.exec(
        select(UserID.id, UserID.name, func.sum(Post.likes_count).label("total_likes"))
        .join(Post, Post.id_usuario == UserID.id)
        .group_by(UserID.id)
        .order_by(func.sum(Post.likes_count).desc())
        .limit(5)
    ).all()

    top_users_by_likes = [
        {"id": row[0], "name": row[1], "total_likes": row[2] or 0}
        for row in top_users_by_likes_raw
    ]

    return {
        "total_posts": total_posts,
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "total_likes": total_likes,
        "top_posts": top_posts,
        "top_users_by_posts": top_users_by_posts,
        "top_users_by_likes": top_users_by_likes,
    }


@stats_router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, session: SessionDep):
    """
    Página principal del dashboard con estadísticas visuales.
    Renderiza templates/dashboard.html con todos los datos calculados.
    """
    data = get_dashboard_data(session)
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=data
    )


@stats_router.get("/json")
async def dashboard_json(session: SessionDep):
    """
    Endpoint JSON con las mismas estadísticas del dashboard.
    Útil para consumir desde el frontend o herramientas externas.
    """
    data = get_dashboard_data(session)
    # Serializar los objetos Post para que sean JSON-friendly
    data["top_posts"] = [
        {
            "contador_post": p.contador_post,
            "contenido": p.contenido,
            "id_usuario": p.id_usuario,
            "likes_count": p.likes_count,
        }
        for p in data["top_posts"]
    ]
    return data