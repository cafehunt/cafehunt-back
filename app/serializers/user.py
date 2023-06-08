from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


class User(UserInDB):
    id: int

    class Config:
        orm_mode = True
