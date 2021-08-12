from identityaccess.domain.service.authorization import AuthorizationService, AuthorizationError
from identityaccess.domain.model.scope import Scope


class AuthorizeCommand:
    def __init__(self, access_token: str, scope: str):
        self.access_token = access_token
        self.scope = scope


class Authorize:
    def __init__(self, authorization_service: AuthorizationService):
        self._authorization_service = authorization_service

    def authorize(self, command: AuthorizeCommand):
        try:
            self._authorization_service.authorize(
                command.access_token,
                Scope(command.scope)
            )
        except AuthorizationError as error:
            raise Exception(str(error))
