# from abc import ABC, abstractmethod
# from uuid import UUID

# from fastapi import HTTPException, Depends, Request, status

# from src.di.dependency_injection import injector
# from src.core.security.session import SessionAdapter, SessionPayload
# from src.di.unit_of_work import AbstractUnitOfWork
# from src.entities.user import User
# from src.errors.auth import UserNotFoundError
# from src.enums import UserRole


# async def authorization(
#     request: Request
# ) -> SessionPayload:
#     adapter = SessionAdapter()
#     session = await adapter.get_session(request)
#     return session


# async def get_auth_user(
#     session: SessionPayload = Depends(authorization)
# ) -> User:
#     user_id = UUID(session.user_id)
#     uow: AbstractUnitOfWork = injector.get(AbstractUnitOfWork)
#     async with uow as auow:
#         user = await auow.auth_repo.get_by_id(id=user_id)
#     if not user:
#         raise UserNotFoundError(user_id)
#     return user


# class BasePermission(ABC):
#     role_error_msg = [{"msg": "You don't have enough permissions"}]
#     role_error_code = status.HTTP_403_FORBIDDEN

#     @abstractmethod
#     def has_required_permissions(self, session: SessionPayload) -> bool: ...

#     def __init__(self, session: SessionPayload):
#         if not hasattr(session, "user_role") or session.user_role is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Cannot determine user role",
#             )
#         if not self.has_required_permissions(session):
#             raise HTTPException(
#                 status_code=self.role_error_code,
#                 detail=self.role_error_msg,
#             )


# class MasterPermission(BasePermission):
#     def has_required_permissions(self, session: SessionPayload) -> bool:
#         return session.user_role == UserRole.master.value


# class ClientPermission(BasePermission):
#     def has_required_permissions(self, session: SessionPayload) -> bool:
#         return session.user_role == UserRole.client.value


# class PermissionsDependency:
#     def __init__(
#         self,
#         permission_classes: list[type[BasePermission]],
#     ):
#         self.permission_classes = permission_classes

#     def __call__(
#         self,
#         session: SessionPayload = Depends(authorization),
#     ) -> None:
#         for perm_cls in self.permission_classes:
#             try:
#                 perm_cls(session)
#                 return
#             except HTTPException:
#                 continue
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You don't have required permissions",
#         )
