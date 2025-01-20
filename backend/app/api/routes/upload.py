from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.core.s3 import S3Client
from app.core.crud import create_media_file
from app.core.models import MediaFileCreate
from app.core.deps import SessionDep, CurrentUser
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from mutagen import File as MutagenFile
import uuid
import os
import io

router = APIRouter()
s3_client = S3Client()

ALLOWED_TYPES = {
    "image": ["image/jpeg", "image/png", "image/webp"],
    "audio": ["audio/mpeg", "audio/wav", "audio/mp3"],
    "video": ["video/mp4", "video/webm", "video/mkv"],
}

def extract_image_exif(file: io.BytesIO):
    try:
        image = Image.open(file)
        exif_data = image._getexif()  # Obtenha os metadados EXIF
        if not exif_data:
            return None
        return {
            key: value for key, value in exif_data.items()
        }
    except Exception as e:
        return {"error": str(e)}

def extract_video_metadata(file_path: str):
    try:
        parser = createParser(file_path)
        if not parser:
            return {"error": "Could not parse file."}
        metadata = extractMetadata(parser)
        if not metadata:
            return None
        return {
            key: metadata.get(key) for key in metadata.exportPlaintext()
        }
    except Exception as e:
        return {"error": str(e)}

def extract_audio_metadata(file_path: str):
    try:
        audio_file = MutagenFile(file_path)
        if not audio_file or not audio_file.tags:
            return None
        return {
            tag: str(value) for tag, value in audio_file.tags.items()
        }
    except Exception as e:
        return {"error": str(e)}

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    session: SessionDep = Depends(),
    current_user: CurrentUser = Depends(),
):
    if file.content_type not in [mime for mimes in ALLOWED_TYPES.values() for mime in mimes]:
        raise HTTPException(400, detail="Tipo de arquivo não suportado.")

    # Gera o nome e o caminho do arquivo no S3
    file_type = file.content_type.split("/")[0]
    filename = f"{file_type}/user_{current_user.id}/{uuid.uuid4().hex}_{file.filename}"

    try:
        # Faz o upload para o S3
        s3_client.upload_fileobj(
            file.file,
            "meu-bucket-s3",
            filename,
            ExtraArgs={"ACL": "public-read"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no upload: {str(e)}")

    # Monta a URL pública do arquivo
    file_url = f"https://meu-bucket-s3.s3.meu-regiao.amazonaws.com/{filename}"

    # Verifica e extrai metadados conforme o tipo de arquivo
    metadata = None
    if file_type == "image":
        file.file.seek(0)  # Reset o ponteiro para o início
        metadata = extract_image_exif(io.BytesIO(file.file.read()))
    elif file_type == "video":
        temp_file_path = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            file.file.seek(0)
            temp_file.write(file.file.read())
        metadata = extract_video_metadata(temp_file_path)
        os.remove(temp_file_path)  # Remove o arquivo temporário após leitura
    elif file_type == "audio":
        temp_file_path = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            file.file.seek(0)
            temp_file.write(file.file.read())
        metadata = extract_audio_metadata(temp_file_path)
        os.remove(temp_file_path)  # Remove o arquivo temporário após leitura

    # Salva os metadados no banco de dados
    media_file = create_media_file(
        session=session,
        filename=file.filename,
        content_type=file.content_type,
        user_id=current_user.id,
        url=file_url,
        file_type=file_type,
        file_extension=file.filename.split(".")[-1].lower(),
    )

    return {
        "url": media_file.url,
        "metadata": metadata,  # Retorna os metadados extraídos, se existirem
    }
