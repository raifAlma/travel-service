from pydantic import BaseModel, EmailStr, model_validator, ConfigDict
from enum import Enum

from api.v1.users.crypto import context


class Gender(str, Enum):
    male = "male"
    female = "female"

class CreateUpdateUserSchema(BaseModel):
    email: EmailStr
    password: str
    username: str
    age: int

    def set_password(self):
        self.password = context.hash(self.password)

    @model_validator(mode='after')
    def check_password(self) -> "CreateUpdateUserSchema":
        self.set_password()
        return self



class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    age: int

class UserInfoSchema(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


