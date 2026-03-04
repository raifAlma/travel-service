from datetime import datetime


from pydantic import BaseModel, model_validator

from api.v1.users.crypto import context


class UserLoginSchema(BaseModel):
    username: str
    password: str
'''
    def set_password(self):
        self.password = context.hash(self.password)

    @model_validator(mode='after')
    def check_password(self) -> "UserLogin":
        self.set_password()
        return self
'''
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    access_token_expires_in: datetime
    refresh_token_expires_in: datetime

class RefreshTokenSchema(BaseModel):

    refresh_token: str