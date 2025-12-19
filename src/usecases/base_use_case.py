from typing import Optional
from src.di.unit_of_work import AbstractUnitOfWork
from src.di.dependency_injection import injector


class BaseUseCase:
    _auow: Optional[AbstractUnitOfWork] = None

    @property
    def async_unit_of_work(self) -> AbstractUnitOfWork:
        if self._auow is None:
            self._auow = injector.get(AbstractUnitOfWork)
        return self._auow
