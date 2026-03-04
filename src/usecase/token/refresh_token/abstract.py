from abc import ABC, abstractmethod

from api.v1.auth.models import RefreshTokenSchema, TokenSchema
from api.v1.users.models import CreateUpdateUserSchema


class AbstractRefreshTokenUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: RefreshTokenSchema) -> TokenSchema:
        ...