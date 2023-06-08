from pydantic import BaseModel


class CafeBase(BaseModel):
    name: str


class Cafe(CafeBase):

    class Config:
        orm_mode = True
