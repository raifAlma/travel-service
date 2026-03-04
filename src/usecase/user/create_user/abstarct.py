from abc import ABC, abstractmethod

from api.v1.users.models import CreateUpdateUserSchema


class AbstractCreateUserUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: CreateUpdateUserSchema):
        ...