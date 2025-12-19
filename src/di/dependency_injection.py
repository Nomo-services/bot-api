# from injector import Injector, Module, provider
# from sqlalchemy.ext.asyncio import AsyncSession
# from src.core.database import IS_RELATIONAL_DB

# from src.repositories.appointment.repository import AppointmentRepository
# from src.repositories.auth.repository import AuthRepository
# from src.repositories.user.repository import UserRepository
# from src.repositories.master.repository import MasterRepository
# from src.repositories.client.repository import ClientRepository
# from src.repositories.client_appointment.repository import ClientAppointmentRepository
# from src.repositories.kv_store.repository import KVStoreRepository
# from src.repositories.speciality.repository import SpecialityRepository
# from src.repositories.service.repository import ServiceRepository

# from .unit_of_work import (
#     AbstractUnitOfWork,
#     AsyncSQLAlchemyUnitOfWork,
# )


# class RelationalDBModule(Module):
#     @provider
#     def provide_async_session(self) -> AsyncSession:
#         from src.core.database import get_async_session

#         return get_async_session()

#     @provider
#     def provide_appointment_repository(self, session: AsyncSession) -> AppointmentRepository:
#         return AppointmentRepository(session)

#     @provider
#     def provide_auth_repository(self, session: AsyncSession) -> AuthRepository:
#         return AuthRepository(session)

#     @provider
#     def provide_user_repository(self, session: AsyncSession) -> UserRepository:
#         return UserRepository(session)

#     @provider
#     def provide_master_repository(self, session: AsyncSession) -> MasterRepository:
#         return MasterRepository(session)

#     @provider
#     def provide_client_repository(self, session: AsyncSession) -> ClientRepository:
#         return ClientRepository(session)

#     @provider
#     def provide_client_appointment_repository(self, session: AsyncSession) -> ClientAppointmentRepository:
#         return ClientAppointmentRepository(session)

#     @provider
#     def provide_kv_store_repository(self, session: AsyncSession) -> KVStoreRepository:
#         return KVStoreRepository(session)

#     @provider
#     def provide_speciality_repository(self, session: AsyncSession) -> SpecialityRepository:
#         return SpecialityRepository(session)

#     @provider
#     def provide_service_repository(self, session: AsyncSession) -> ServiceRepository:
#         return ServiceRepository(session)

#     @provider
#     def provide_async_sqlalchemy_unit_of_work(
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
#     ) -> AbstractUnitOfWork:
#         return AsyncSQLAlchemyUnitOfWork(
#             session=session,
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


# class DatabaseModuleFactory:
#     def create_module(self):
#         if IS_RELATIONAL_DB:
#             return RelationalDBModule()


# injector = Injector([DatabaseModuleFactory().create_module()])
