from identityaccess.domain.service.authentication import AuthenticationService, AuthenticationError
from identityaccess import InvalidRequestParamsException, ErrorCodes
from identityaccess.domain.service.token_generator import TokenGenerator
from identityaccess.domain.model.tenant import TenantId


class AuthenticateCommand:
    def __init__(self, tenant_id: str, username: str, password: str):
        self.password = password
        self.username = username
        self.tenant_id = tenant_id


class AuthenticateResponse:
    def __init__(self, token_type: str, access_token: str):
        self.token_type = token_type
        self.access_token = access_token


class Authenticate:
    def __init__(
        self,
        authentication_service: AuthenticationService,
        token_generator: TokenGenerator
    ):
        self._authentication_service = authentication_service
        self._token_generator = token_generator

    def authenticate(self, command: AuthenticateCommand) -> AuthenticateResponse:
        _ensure_all_values_are_provided(command)

        try:
            tenant_id = TenantId(command.tenant_id)
        except ValueError as error:
            raise InvalidRequestParamsException(
                ErrorCodes.INVALID_REQUEST_PARAMETER,
                details=str(error)
            )

        user_descriptor = self._authentication_service.authenticate(
            tenant_id,
            command.username,
            command.password
        )

        return AuthenticateResponse(
            self._token_generator.TOKEN_TYPE,
            self._token_generator.generate(user_descriptor)
        )


def _ensure_all_values_are_provided(command: AuthenticateCommand) -> None:
    if not command.tenant_id:
        raise InvalidRequestParamsException(ErrorCodes.MISSING_REQUEST_PARAMETER, "A tenant id must be provided")

    if not command.username:
        raise InvalidRequestParamsException(ErrorCodes.MISSING_REQUEST_PARAMETER, "A username must be provided")

    if not command.password:
        raise InvalidRequestParamsException(ErrorCodes.MISSING_REQUEST_PARAMETER, "A password must be provided")
