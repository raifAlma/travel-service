from enum import Enum
from typing import Optional

from api.v1.users.crypto import context
from pydantic import BaseModel, ConfigDict, EmailStr, model_validator


class Gender(str, Enum):
    male = "male"
    female = "female"


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str
    username: str
    age: int

    def set_password(self):
        self.password = context.hash(self.password)

    @model_validator(mode="after")
    def check_password(self) -> "CreateUserSchema":
        self.set_password()
        return self


class UpdateUserSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    password: Optional[str] = None

class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    age: int


class UserInfoSchema(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
