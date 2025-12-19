# from abc import ABC, abstractmethod
# from typing import Any

# from sqlalchemy.ext.asyncio import AsyncSession

# from src.repositories.abstraction.appointment import AbstractAppointmentRepository
# from src.repositories.abstraction.auth import AbstractAuthRepository
# from src.repositories.abstraction.user import AbstractUserRepository
# from src.repositories.abstraction.master import AbstractMasterRepository
# from src.repositories.abstraction.client import AbstractClientRepository
# from src.repositories.abstraction.client_appointment import AbstractClientAppointmentRepository
# from src.repositories.abstraction.kv_store import AbstractKVStoreRepository
# from src.repositories.abstraction.speciality import AbstractSpecialityRepository
# from src.repositories.abstraction.service import AbstractServiceRepository

# from src.repositories.appointment.repository import AppointmentRepository
# from src.repositories.auth.repository import AuthRepository
# from src.repositories.user.repository import UserRepository
# from src.repositories.master.repository import MasterRepository
# from src.repositories.client.repository import ClientRepository
# from src.repositories.client_appointment.repository import ClientAppointmentRepository
# from src.repositories.kv_store.repository import KVStoreRepository
# from src.repositories.speciality.repository import SpecialityRepository
# from src.repositories.service.repository import ServiceRepository


# class AbstractUnitOfWork(ABC):
#     appointment_repo: AbstractAppointmentRepository
#     auth_repo: AbstractAuthRepository
#     user_repo: AbstractUserRepository
#     master_repo: AbstractMasterRepository
#     client_repo: AbstractClientRepository
#     client_appointment_repo: AbstractClientAppointmentRepository
#     kv_store_repo: AbstractKVStoreRepository
#     speciality_repo: AbstractSpecialityRepository
#     service_repo: AbstractServiceRepository

#     def __init__(
#         self,
#         appointment_repo: AbstractAppointmentRepository,
#         auth_repo: AbstractAuthRepository,
#         user_repo: AbstractUserRepository,
#         master_repo: AbstractMasterRepository,
#         client_repo: AbstractClientRepository,
#         client_appointment_repo: AbstractClientAppointmentRepository,
#         kv_store_repo: AbstractKVStoreRepository,
#         speciality_repo: AbstractSpecialityRepository,
#         service_repo: AbstractServiceRepository,
#     ):
#         self.appointment_repo = appointment_repo
#         self.auth_repo = auth_repo
#         self.user_repo = user_repo
#         self.master_repo = master_repo
#         self.client_repo = client_repo
#         self.client_appointment_repo = client_appointment_repo
#         self.kv_store_repo = kv_store_repo
#         self.speciality_repo = speciality_repo
#         self.service_repo = service_repo

#     @abstractmethod
#     async def __aenter__(self) -> "AbstractUnitOfWork":
#         raise NotImplementedError

#     @abstractmethod
#     async def __aexit__(self, exc_type, exc, tb):
#         raise NotImplementedError


# class AsyncSQLAlchemyUnitOfWork(AbstractUnitOfWork):
#     def __init__(
#         self,
#         session: AsyncSession,
#         appointment_repo: AppointmentRepository,
#         auth_repo: AuthRepository,
#         user_repo: UserRepository,
#         master_repo: MasterRepository,
#         client_repo: ClientRepository,
#         client_appointment_repo: ClientAppointmentRepository,
#         kv_store_repo: KVStoreRepository,
#         speciality_repo: SpecialityRepository,
#         service_repo: ServiceRepository,
#     ):
#         super().__init__(
#             appointment_repo=appointment_repo,
#             auth_repo=auth_repo,
#             user_repo=user_repo,
#             master_repo=master_repo,
#             client_repo=client_repo,
#             client_appointment_repo=client_appointment_repo,
#             kv_store_repo=kv_store_repo,
#             speciality_repo=speciality_repo,
#             service_repo=service_repo,
#         )
#         self._session = session

#     async def __aenter__(self):
#         return self

#     async def __aexit__(
#         self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any
#     ):
#         try:
#             if exc_type is None:
#                 await self._session.commit()
#             else:
#                 await self._session.rollback()
#         finally:
#             await self._session.close()
#             await self.remove()

#     async def remove(self):
#         from src.core.database import AsyncScopedSession

#         await AsyncScopedSession.remove()
