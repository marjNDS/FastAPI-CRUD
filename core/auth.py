from pytz import timezone


from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.usuario_model import UsuarioModel
from core.configs import settings
from core.security import verificar_senha

from pydantic import EmailStr


# Cria um endpoint para autenticação, utilizando o token de acesso
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

# Função assíncrona para autenticar um usuário
async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    # Cria uma sessão assíncrona com o banco de dados
    async with db as session:
        # Define a consulta para selecionar o usuário com o e-mail fornecido
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        # Executa a consulta
        result = await session.execute(query)
        # Obtém o usuário único ou nenhum
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        # Se o usuário não for encontrado, retorna None
        if not usuario:
            return None

        # Se a senha não corresponder, retorna None
        if not verificar_senha(senha, usuario.senha):
            return None

        # Retorna o usuário se as credenciais estiverem corretas
        return usuario

# Função privada para criar um token JWT
def _criar_token(tipo_token: str, tempo_vida: timedelta, usuario: str) -> str:
    payload = {}  # Dicionário para armazenar os dados do token
    sp = timezone('America/Sao_Paulo')  # Define o fuso horário para São Paulo
    expira = datetime.now(tz=sp) + tempo_vida  # Calcula a data de expiração do token

    # Define os dados do token
    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(usuario)

    # Codifica o token usando a chave secreta e o algoritmo especificado
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

# Função para criar um token de acesso
def criar_token_acesso(sub: str) -> str:
    return _criar_token(
        tipo_token='access_token',  # Define o tipo do token como "access_token"
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),  # Define o tempo de vida do token
        usuario=sub  # Define o usuário associado ao token
    )
