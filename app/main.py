from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.database import engine, Base
from fastapi_pagination import add_pagination

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://cafehunt.pp.ua",
    "http://www.cafehunt.pp.ua",
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
add_pagination(app)


@app.on_event("startup")
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
