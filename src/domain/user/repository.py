from abc import ABC, abstractmethod

from domain.repository.abstract import AbstractRepository, TCreateDTO, TEntity

from .models import User, UserCreateDTO, UserUpdateDTO



class AbstractUserRepository(
    AbstractRepository[User, int, UserCreateDTO, UserUpdateDTO],
    ABC,
):
    @abstractmethod
    def create(self, dto: TCreateDTO) -> TEntity:
        raise NotImplementedError()
    ...

    @abstractmethod
    def get_by_id(self, id: int) -> User:
        raise NotImplementedError()
    ...

    @abstractmethod
    def get_by_name(self, name: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def put_by_id(self, id: int, data: UserCreateDTO) -> None:
        raise NotImplementedError()


    """
    Контракт репозитория для Item.

    Сейчас просто наследуем общий AbstractRepository.
    Если потом понадобятся доменные методы (find_by_title и т.п.) —
    добавить сюда.
    """

    # пример доменного метода на будущее:
    # @abstractmethod
    # def find_by_title(self, title: str) -> List[Item]:
    #     raise NotImplementedError
    ...