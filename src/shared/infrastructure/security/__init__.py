from functools import wraps
from flask import request
import credential_shield as cs

from shared.infrastructure.application.settings import settings
from shared.application.errors import ErrorCodes, ApiBaseError
from shared.domain.user import User


class AuthorizationError(ApiBaseError):
    pass


class ExpiredTokenException(ApiBaseError):
    pass


def authorization_required(scope: str):
    def decorator(func):
        @wraps(func)
        def decorated_function(self, *args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise AuthorizationError(ErrorCodes.ACCESS_TOKEN_NOT_PROVIDED)

            token_validator = cs.TokenValidator(
                settings.application_id(),
                scope,
                settings.token_issuer()
            )

            try:
                token_data: cs.TokenData = token_validator.validate(auth_header, settings.public_key())
                user = User(
                    token_data.tenant_id(),
                    token_data.username(),
                    token_data.user_email()
                )

                return func(self, user, *args, **kwargs)
            except cs.ExpiredTokenException:
                raise ExpiredTokenException(ErrorCodes.ACCESS_TOKEN_EXPIRED)
            except cs.CredentialShieldException as error:
                raise AuthorizationError(ErrorCodes.AUTHORIZATION_FAILED, details=str(error))

        return decorated_function

    return decorator
