from typing import Generator, Optional

from fastapi import Depends, HTTPException, status

from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from pydantic import Session, BaseModel

from core.database import Session
from core.auth import oauth2_schema
from core.configs import settings
from models.usuario_model import UsuarioModel


# Define o modelo de dados para o token, com um campo opcional username
class TokenData(BaseModel):
    username: Optional[str] = None

# Função assíncrona para obter uma sessão de banco de dados
async def get_session() -> Generator:
    session: AsyncSession = Session()  # Cria uma nova sessão assíncrona
    try:
        yield session  # Fornece a sessão para ser usada no contexto atual
    finally:
        await session.close()  # Garante que a sessão será fechada após o uso

# Função assíncrona para obter o usuário atual autenticado com base no token JWT
async def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_schema)) -> UsuarioModel:
    # Define uma exceção HTTP 401 para ser usada em caso de falha na autenticação
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # Decodifica o token JWT usando a chave secreta e o algoritmo especificado
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )

        # Obtém o nome de usuário do payload do token
        username: str = payload.get("sub")

        # Se o nome de usuário não estiver presente, lança a exceção de credenciais
        if username is None:
            raise credential_exception

        # Cria uma instância de TokenData com o nome de usuário
        token_data: TokenData = TokenData(username=username)

    except JWTError:
        # Se houver um erro ao decodificar o token, lança a exceção de credenciais
        raise credential_exception

    # Cria uma sessão assíncrona com o banco de dados
    async with db as session:
        # Define a consulta para selecionar o usuário com o ID correspondente ao nome de usuário do token
        query = select(UsuarioModel).filter(UsuarioModel.id == int(token_data.username))
        # Executa a consulta
        result = await session.execute(query)
        # Obtém o usuário único ou nenhum
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        # Se o usuário não for encontrado, lança a exceção de credenciais
        if usuario is None:
            raise credential_exception

        # Retorna o usuário autenticado
        return usuario
