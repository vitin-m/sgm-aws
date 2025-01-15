from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.core.s3 import S3Client
from app.core.crud import create_media_file
from app.core.models import MediaFileCreate
from app.core.deps import SessionDep, CurrentUser
import uuid

router = APIRouter()
s3_client = S3Client()

ALLOWED_TYPES = {
    "image": ["image/jpeg", "image/png", "image/webp"],
    "audio": ["audio/mpeg", "audio/wav"],
    "video": ["video/mp4", "video/webm"],
}

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

    return {"url": media_file.url}
