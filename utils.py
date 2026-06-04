import os
from pathlib import Path
import shutil
from fastapi import File, UploadFile, HTTPException
from supabase import create_client
from dotenv import load_dotenv
import uuid

load_dotenv()

IMG_DIR = Path("files/img")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")


def save_img_local(file: UploadFile):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Archivo Invalido")

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    dest = IMG_DIR / file.filename

    with dest.open("wb") as store:
        shutil.copyfileobj(file.file, store)

    return dest


def supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError("No credentials")
    return create_client(url, key)


def save_img_remote(file: UploadFile):
    # Valida que sea una imagen antes de intentar subir
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Archivo Invalido")

    try:
        contents = file.file.read()
        extension = file.filename.split(".")[-1]
        path = f"{uuid.uuid4()}.{extension}"

        supa_client = supabase_client()

        supa_client.storage.from_(SUPABASE_BUCKET).upload(
            path=path,
            file=contents,
            file_options={"content-type": file.content_type}
        )

        stored_url_bucket = (supa_client
                             .storage
                             .from_(SUPABASE_BUCKET)
                             .get_public_url(path))

        return stored_url_bucket

    except RuntimeError:
        # Credenciales de Supabase no configuradas
        raise HTTPException(status_code=500, detail="Error de configuración del servidor de imágenes")

    except Exception:
        # Cualquier fallo de red o Supabase — no tumba el servidor,
        # el post/usuario se crea igual pero sin imagen
        return None