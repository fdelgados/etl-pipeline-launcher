import jwt

from identityaccess.domain.model.tenant import TenantId
from identityaccess.domain.model.role import Role
from identityaccess.domain.model.scope import Scope
from identityaccess.domain.model.access_token import AccessToken

from identityaccess.domain.service.permission_checker import PermissionDeniedError, PermissionChecker
from identityaccess.domain.service.authorization import AuthorizationService, AuthorizationError
from shared.infrastructure.application.settings import Settings

from identityaccess import ErrorCodes


class JwtAuthorizationService(AuthorizationService):
    def __init__(self, permission_checker: PermissionChecker):
        self._permission_checker = permission_checker

    def authorize(self, tenant_id: TenantId, access_token: AccessToken, scope: Scope) -> None:
        if not access_token.is_bearer():
            raise AuthorizationError(ErrorCodes.INVALID_ACCESS_TOKEN_TYPE)

        try:
            payload = jwt.decode(
                access_token.value,
                Settings.secret_key(),
                algorithms=['HS256'],
                options={
                    'require': ['sub', 'role', 'exp', 'iat'],
                    'verify_exp': True
                }
            )

            token_tenant_id = TenantId(str(payload.get('sub')))

            if token_tenant_id != tenant_id:
                raise AuthorizationError(ErrorCodes.TENANT_ID_MISMATCH)

            role = Role(str(payload.get('role')))

            self._permission_checker.check(tenant_id, role, scope)

        except (jwt.DecodeError, jwt.MissingRequiredClaimError) as error:
            raise AuthorizationError(ErrorCodes.INVALID_ACCESS_TOKEN, details=str(error))
        except jwt.ExpiredSignatureError as error:
            raise AuthorizationError(ErrorCodes.ACCESS_TOKEN_EXPIRED, details=str(error))
        except PermissionDeniedError as error:
            raise AuthorizationError.create_from_error(error)
