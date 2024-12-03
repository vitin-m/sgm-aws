from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core import settings


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PATH}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Configuração do CORS
origins = ["*"]  # Permitir todas as origens

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Inclua o roteador da API
app.include_router(api_router, prefix=settings.API_PATH)

# Outras configurações e inicializações do aplicativo
