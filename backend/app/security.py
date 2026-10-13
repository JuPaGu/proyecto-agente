import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

from app import config

bearer = HTTPBearer(auto_error=False)
jwks_client = PyJWKClient(config.KEYCLOAK_JWKS_URL)


def usuario_actual(
    cred: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict:
    no_autorizado = HTTPException(
        status_code=401,
        detail="Token inválido o ausente.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if cred is None:
        raise no_autorizado
    try:
        clave = jwks_client.get_signing_key_from_jwt(cred.credentials)
        datos = jwt.decode(
            cred.credentials,
            clave.key,
            algorithms=["RS256"],
            issuer=config.KEYCLOAK_ISSUER,
            options={"verify_aud": False, "require": ["exp", "iss", "sub"]},
        )
    except jwt.PyJWTError:
        raise no_autorizado
    if datos.get("azp") != config.KEYCLOAK_CLIENT_ID:
        raise no_autorizado
    return {"id": datos["sub"], "usuario": datos.get("preferred_username")}