from abc import ABC, abstractmethod

from api.v1.users.models import UpdateUserSchema


class AbstractUpdateUserUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: UpdateUserSchema): ...
