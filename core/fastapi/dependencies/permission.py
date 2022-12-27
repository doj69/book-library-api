from abc import ABC, abstractmethod
from typing import List

from fastapi import Request
from fastapi.openapi.models import (
    OAuth2,
    OAuthFlowPassword,
    OAuthFlows,
    SecuritySchemeType,
)
from fastapi.security.base import SecurityBase

from app.user.service import UserService
from core.exceptions import CustomException, UnauthorizedException


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List, permision_code: str | None = None):
        self.permissions = permissions
        self.permision_code = permision_code
        self.model: OAuth2 = OAuth2(
            type=SecuritySchemeType.oauth2,
            flows=OAuthFlows(
                password=OAuthFlowPassword(tokenUrl="api/v1/auth/login")
            ),
        )
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        for permission in self.permissions:
            cls = permission()
            if self.permision_code:
                if not await cls.has_permission(
                    request=request, permission_code=self.permision_code
                ):
                    raise cls.exception
            elif not await cls.has_permission(request=request):
                raise cls.exception


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.id is not None


class IsRolePermissionGranted(BasePermission):
    exception = UnauthorizedException

    async def has_permission(
        self, request: Request, permission_code: str
    ) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        return await UserService().is_role_permissions_granted(
            user_id=user_id, allowed_permission=permission_code
        )
