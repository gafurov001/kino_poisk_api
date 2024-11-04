from typing import Optional

from pydantic import BaseModel


class UserAuth(BaseModel):
    name: str
    username: str
    password: str
    email: str

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    name: str
    username: str
    email: str

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    exp: Optional[int]

class SystemUser(BaseModel):
    id: int
    name: str
    username: str
    email: str

    class Config:
        from_attributes = True

class KinopoiskID(BaseModel):
    kinopoisk_id: int

    class Config:
        from_attributes = True
