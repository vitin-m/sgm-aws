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
import datetime

router = APIRouter()
s3_client = S3Client()

ALLOWED_TYPES = {
    "image": ["image/jpeg", "image/png", "image/webp"],
    "audio": ["audio/mpeg", "audio/wav"],
    "video": ["video/mp4", "video/webm"],
}

THUMBNAIL_SIZE = (150, 150)  # Tamanho da miniatura em pixels


def generate_thumbnail(image_data: io.BytesIO):
    """Gera uma miniatura para imagens."""
    try:
        image = Image.open(image_data)
        image.thumbnail(THUMBNAIL_SIZE)
        thumbnail_data = io.BytesIO()
        image.save(thumbnail_data, format=image.format)
        thumbnail_data.seek(0)
        return thumbnail_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar miniatura: {str(e)}")


def extract_image_exif(image_data: io.BytesIO):
    """Extrai os dados EXIF de uma imagem."""
    try:
        image = Image.open(image_data)
        exif_data = image._getexif() or {}
        exif_metadata = {
            "ExifVersion": exif_data.get(0x9000),
            "DateTime": exif_data.get(0x9003),
            "Make": exif_data.get(0x010F),
            "Model": exif_data.get(0x0110),
            "GPS": exif_data.get(0x0002),  # Exemplo de dados de localização GPS (se presentes)
        }
        return exif_metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao extrair EXIF: {str(e)}")


def extract_video_metadata(file_path):
    """Extrai os metadados de um vídeo."""
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        video_metadata = {
            "duration": metadata.get('duration'),
            "resolution": f"{metadata.get('width')}x{metadata.get('height')}",
            "frame_rate": metadata.get('frame_rate'),
            "video_codec": metadata.get('codec'),
            "audio_codec": metadata.get('audio_codec'),
            "bit_rate": metadata.get('bit_rate'),
        }
        return video_metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao extrair metadados do vídeo: {str(e)}")


def extract_audio_metadata(file_path):
    """Extrai os metadados de um arquivo de áudio."""
    try:
        audio = MutagenFile(file_path)
        audio_metadata = {
            "duration": audio.info.length,
            "bit_rate": audio.info.bitrate,
            "sample_rate": audio.info.sample_rate,
            "channels": audio.info.channels,
        }
        return audio_metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao extrair metadados do áudio: {str(e)}")


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

    # Propriedades e metadados específicos conforme o tipo de arquivo
    file_properties = {
        "filename": file.filename,
        "size": file.size,
        "upload_date": datetime.datetime.utcnow().isoformat(),
        "mime_type": file.content_type,
    }

    metadata = None
    thumbnail_url = None

    if file_type == "image":
        file.file.seek(0)
        metadata = extract_image_exif(io.BytesIO(file.file.read()))

        # Gerar miniatura
        file.file.seek(0)  # Resetar o ponteiro
        thumbnail_data = generate_thumbnail(io.BytesIO(file.file.read()))
        thumbnail_filename = f"thumbnail/user_{current_user.id}/{uuid.uuid4().hex}_thumbnail_{file.filename}"
        try:
            s3_client.upload_fileobj(
                thumbnail_data,
                "meu-bucket-s3",
                thumbnail_filename,
                ExtraArgs={"ACL": "public-read"},
            )
            thumbnail_url = f"https://meu-bucket-s3.s3.meu-regiao.amazonaws.com/{thumbnail_filename}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao fazer upload da miniatura: {str(e)}")

    elif file_type == "video":
        temp_file_path = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            file.file.seek(0)
            temp_file.write(file.file.read())
        metadata = extract_video_metadata(temp_file_path)
        os.remove(temp_file_path)  # Remover o arquivo temporário após leitura

    elif file_type == "audio":
        temp_file_path = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            file.file.seek(0)
            temp_file.write(file.file.read())
        metadata = extract_audio_metadata(temp_file_path)
        os.remove(temp_file_path)  # Remover o arquivo temporário após leitura

    # Salvar os metadados no banco de dados
    media_file = create_media_file(
        session=session,
        filename=file.filename,
        content_type=file.content_type,
        user_id=current_user.id,
        url=file_url,
        file_type=file_type,
        file_extension=file.filename.split(".")[-1].lower(),
        properties=file_properties,  # Salvar propriedades gerais
    )

    return {
        "url": media_file.url,
        "metadata": metadata,
        "thumbnail_url": thumbnail_url,  # Retornar a URL da miniatura para imagens
    }