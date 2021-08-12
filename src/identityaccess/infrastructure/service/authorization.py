import jwt

from identityaccess.domain.model.tenant import TenantId, TenantRepository
from identityaccess.domain.model.role import Role
from identityaccess.domain.model.scope import Scope

from identityaccess.infrastructure.service.permission_checker import PermissionDeniedError, PermissionChecker
from identityaccess.domain.service.authorization import AuthorizationService, AuthorizationError
from shared.infrastructure.application.settings import Settings


class JwtAuthorizationService(AuthorizationService):
    def __init__(
        self,
        tenant_repository: TenantRepository,
        permission_checker: PermissionChecker
    ):
        self._tenant_repository = tenant_repository
        self._permission_checker = permission_checker

    def authorize(self, access_token: str, scope: Scope) -> None:
        token_type, auth_token = access_token.split()

        if token_type != "Bearer":
            raise AuthorizationError("Access token must be of type Bearer")

        try:
            payload = jwt.decode(
                auth_token,
                Settings.secret_key(),
                algorithms=["HS256"]
            )

            tenant_id = TenantId(str(payload.get("sub")))
            role = Role(str(payload.get("role")))

            self._permission_checker.check(tenant_id, role, scope)

        except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, PermissionDeniedError) as error:
            raise AuthorizationError(str(error))
