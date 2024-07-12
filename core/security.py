from passlib.context import CryptContext

CRYPTO = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verificar_senha(senha: str, hash_senha: str) -> bool:
    """Verifica se as senhas batem, comparando a senha informada com o hash presente no banco de dados

    Args:
        senha (str): senha informada
        hash_senha (str): senha hasheada no bd

    Returns:
        bool: true se forem iguais, false se diferirem.
    """

    return CRYPTO.verify(senha, hash_senha)


def gerar_hash_senha(senha: str) -> str:
    """retorna a versão hasheada da senha informada pelo usuário

    Args:
        senha (str): senha informada pelo usuário

    Returns:
        str: hash gerado a partir da senha
    """
    return CRYPTO.hash(senha)
