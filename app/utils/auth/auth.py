from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication import JWTStrategy

import secrets

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


SECRET = secrets.token_urlsafe(32)  # should be set as an environment variable


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)
