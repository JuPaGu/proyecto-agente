import os

KEYCLOAK_ISSUER = os.getenv("KEYCLOAK_ISSUER", "http://localhost:8080/realms/agente-espacio")
KEYCLOAK_JWKS_URL = os.getenv(
    "KEYCLOAK_JWKS_URL", f"{KEYCLOAK_ISSUER}/protocol/openid-connect/certs"
)
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "agente-frontend")
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]