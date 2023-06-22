from pydantic import BaseModel


class City(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
