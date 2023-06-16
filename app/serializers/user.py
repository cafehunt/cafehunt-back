import re
from typing import Optional

from fastapi_users import schemas
from pydantic import validator


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str
    phone_number: Optional[str] = None


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    phone_number: Optional[str] = None

    @validator("phone_number")
    def validate_phone_number(cls, phone_number):
        if phone_number is not None:
            if not re.fullmatch(r"\+[0-9]{8,15}", phone_number):
                raise ValueError("Phone number must start with '+' followed by 8 to 15 digits")
        return phone_number

    @validator("password")
    def validate_password(cls, value: str):
        if len(value) < 8 or len(value) > 30:
            raise ValueError("Password must be between 8 and 30 characters")
        if not re.search("[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search("[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search("[0-9]", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search("[@#$?!]", value):
            raise ValueError("Password must contain at least one special character (@, #, $, ?, !)")
        return value


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
