from identityaccess.domain.service.authorization import AuthorizationService, AuthorizationError
from identityaccess.domain.model.scope import Scope
from identityaccess.domain.model.tenant import TenantId
from identityaccess.domain.model.access_token import AccessToken

from identityaccess import InvalidRequestParamsException, ErrorCodes


class AuthorizeCommand:
    def __init__(self, tenant_id: str, access_token: str, scope: str):
        self.tenant_id = tenant_id
        self.access_token = access_token
        self.scope = scope


class Authorize:
    def __init__(self, authorization_service: AuthorizationService):
        self._authorization_service = authorization_service

    def authorize(self, command: AuthorizeCommand) -> None:
        self._ensure_command_values_are_supplied(command)

        try:
            self._authorization_service.authorize(
                TenantId(command.tenant_id.strip()),
                AccessToken(command.access_token.strip()),
                Scope(command.scope.strip())
            )
        except ValueError as error:
            raise InvalidRequestParamsException(ErrorCodes.INVALID_REQUEST_PARAMETER, details=str(error))

    def _ensure_command_values_are_supplied(self, command: AuthorizeCommand):
        if not command.tenant_id:
            raise InvalidRequestParamsException(ErrorCodes.MISSING_REQUEST_PARAMETER, 'A tenant id must be provided')

        if not command.access_token:
            raise InvalidRequestParamsException(
                ErrorCodes.MISSING_REQUEST_PARAMETER,
                'An access token must be provided'
            )

        if not command.scope:
            raise InvalidRequestParamsException(ErrorCodes.MISSING_REQUEST_PARAMETER, 'A scope must be provided')
