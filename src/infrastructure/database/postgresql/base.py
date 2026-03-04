from sqlalchemy.orm import declarative_base

Base = declarative_base()

from infrastructure.database.postgresql.models.token import Token
from infrastructure.database.postgresql.models.users import User
from infrastructure.database.postgresql.models.Route import Route