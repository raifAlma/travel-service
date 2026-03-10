from datetime import datetime
from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    username: str
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    access_token_expires_in: datetime
    refresh_token_expires_in: datetime

class RefreshTokenSchema(BaseModel):

    refresh_token: str