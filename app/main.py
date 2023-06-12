from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from app.api import api_router
from app.core.database import engine, Base
from app.core.user_manager import get_user_manager
from app.models.user import User
from app.serializers.user import UserRead, UserCreate, UserUpdate
from app.utils.auth.auth import auth_backend

app = FastAPI()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(api_router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.on_event("startup")
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
