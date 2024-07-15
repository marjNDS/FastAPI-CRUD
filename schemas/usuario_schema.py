from typing import Optional, List

from pydantic import BaseModel, EmailStr

from schemas.artigo_schema import ArtigoSchema


class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True

# para criar uma conta


class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str


class UsuarioSchemaArtigos(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]


# para atualizar dados no bd
class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[str]
    senha: Optional[str]
    is_admin: Optional[bool]
