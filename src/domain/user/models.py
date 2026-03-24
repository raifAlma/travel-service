from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class User:
    id: int
    title: str
    description: str


@dataclass(slots=True)
class UserCreateDTO:
    title: str
    description: str


@dataclass(slots=True)
class UserUpdateDTO:
    title: Optional[str] = None
    description: Optional[str] = None
