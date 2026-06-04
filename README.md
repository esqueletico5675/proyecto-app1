# proyecto-app1 — Red Social Minimalista

API REST + interfaz web construida con **FastAPI**, **SQLModel** y **SQLite/PostgreSQL (Neon)**. Permite crear usuarios, publicar posts, dar likes, buscar contenido y ver estadísticas en un dashboard.

---

## Tecnologías

- Python 3.11+
- FastAPI — framework web
- SQLModel — ORM sobre SQLAlchemy
- Jinja2 — templates HTML
- Cloudinary — almacenamiento de imágenes remotas
- SQLite (local) / PostgreSQL Neon (producción)

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/esqueletico5675/proyecto-app1.git
cd proyecto-app1

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu DATABASE_URL y credenciales de Cloudinary

# 5. Ejecutar
uvicorn main:app --reload
```

La app queda disponible en `http://localhost:8000`.  
Documentación interactiva en `http://localhost:8000/docs`.

---

## Variables de entorno (`.env`)

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | URL de conexión PostgreSQL (Neon) o `sqlite:///apk.sqlite3` para local |
| `CLOUDINARY_CLOUD_NAME` | Nombre del cloud en Cloudinary |
| `CLOUDINARY_API_KEY` | API Key de Cloudinary |
| `CLOUDINARY_API_SECRET` | API Secret de Cloudinary |

---

## Estructura del proyecto

```
proyecto-app1/
├── main.py            # Rutas web y API REST
├── models.py          # Modelos SQLModel (UserID, Post, etc.)
├── operation.py       # Lógica de negocio / acceso a BD
├── db.py              # Configuración del motor y sesión
├── stats_router.py    # Router de estadísticas (Criterio 15)
├── utils.py           # Helpers para subida de imágenes
├── templates/         # HTML con Jinja2
│   ├── index.html
│   ├── usuarios.html
│   ├── posts.html
│   ├── dashboard.html
│   └── ...
├── requirements.txt
└── .env
```

---

## Diagrama de modelos

```
┌──────────────────────────────┐        ┌──────────────────────────────────┐
│           UserID             │        │              Post                │
├──────────────────────────────┤        ├──────────────────────────────────┤
│ id          INT  PK          │◄──┐    │ contador_post  INT  PK           │
│ name        STR  (1-15 chars)│   └────│ id_usuario     INT  FK→UserID.id │
│ pin         INT              │        │ contenido      STR               │
│ image_url   STR  nullable    │        │ pin            INT               │
│ activo      BOOL default=True│        │ likes_count    INT  default=0    │
└──────────────────────────────┘        │ image_url      STR  nullable     │
                                        └──────────────────────────────────┘
```

Un **UserID** puede tener muchos **Post** (relación 1:N).  
El campo `activo` implementa soft-delete: el usuario no se borra físicamente.

---

## Dashboard de Estadísticas

La app incluye un dashboard en `/stats` accesible desde la barra de navegación. Muestra en tiempo real:

- **Total de posts** publicados en la plataforma
- **Total de usuarios** registrados (activos e inactivos)
- **Usuarios activos** — con acceso habilitado
- **Usuarios inactivos** — dados de baja (soft-delete)
- **Total de likes** acumulados en todos los posts
- **Top 5 posts** con más likes
- **Top 5 usuarios** por cantidad de posts publicados
- **Top 5 usuarios** por likes totales recibidos

También disponible como JSON en `/stats/json` para consumo externo.

---

## Endpoints documentados

### Vistas web (HTML)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Página de inicio |
| GET | `/usuarios` | Lista de usuarios |
| GET | `/usuarios/{id}` | Perfil de un usuario con sus posts |
| GET | `/posts` | Feed de todos los posts |
| GET | `/buscar?word=texto` | Buscar posts por palabra clave |
| GET | `/stats` | Dashboard de estadísticas |

### Formularios (HTML POST)

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/form/crear-usuario` | Crear usuario (name, pin, imagen) |
| POST | `/form/crear-post` | Publicar post (user_id, contenido, imagen) |
| GET/POST | `/usuarios/{id}/editar` | Editar nombre/imagen (requiere PIN) |
| GET/POST | `/posts/{id}/editar` | Editar contenido de post (requiere PIN) |
| POST | `/posts/{id}/borrar` | Eliminar post (requiere PIN) |
| POST | `/form/borrar-usuario/{id}` | Desactivar usuario (requiere PIN) |
| POST | `/posts/{id}/like` | Dar like a un post |
| POST | `/posts/{id}/quitar-like` | Quitar like a un post |

### API REST (JSON)

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/CREATE_USERS` | Crear usuario |
| GET | `/SHOW_ALL_USERS` | Listar todos los usuarios |
| GET | `/FIND_USER/{id}` | Buscar usuario por ID (incluye posts) |
| GET | `/User_active/` | Usuarios activos |
| GET | `/User_inactive/` | Usuarios inactivos |
| PATCH | `/UPDATE_USER/{id}` | Actualizar usuario |
| DELETE | `/DELETE_USER/{id}` | Soft-delete usuario |
| POST | `/CREATE_POST` | Crear post |
| GET | `/SHOW_ALL_POSTS` | Listar todos los posts |
| GET | `/FIND_POST/{id}` | Buscar post por ID |
| GET | `/Search_WithWord/?word=texto` | Buscar posts por palabra |
| PATCH | `/UPDATE_POST/{id}` | Actualizar post |
| DELETE | `/DELETE_POST/{id}` | Eliminar post |

### Estadísticas

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/stats` | Dashboard HTML con métricas |
| GET | `/stats/json` | Mismas métricas en JSON |

### Imágenes

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/image/local` | Guardar imagen localmente |
| POST | `/image/remote` | Subir imagen a Cloudinary |

---

## Flujo de autenticación (PIN)

Este proyecto usa un sistema simple de **PIN numérico** en lugar de tokens JWT. Al crear un usuario, se establece un PIN. Ese mismo PIN se hereda en todos sus posts. Para editar o borrar cualquier contenido, se debe proveer el PIN correcto.

---

## Licencia

MIT