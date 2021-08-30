from functools import wraps
from flask import request
import credential_shield as cs

from shared import settings
from shared import ApiErrorCodes, ApiBaseError
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
                raise AuthorizationError(ApiErrorCodes.ACCESS_TOKEN_NOT_PROVIDED)

            token_validator = cs.TokenValidator(
                settings.application_id(),
                scope,
                settings.token_issuer()
            )

            try:
                token: cs.Token = token_validator.validate(auth_header, settings.public_key())
                user = User(
                    token.tenant_id(),
                    token.username(),
                    token.user_email()
                )

                return func(self, user, *args, **kwargs)
            except cs.ExpiredTokenException:
                raise ExpiredTokenException(ApiErrorCodes.ACCESS_TOKEN_EXPIRED)
            except cs.CredentialShieldException as error:
                raise AuthorizationError(ApiErrorCodes.AUTHORIZATION_FAILED, details=str(error))

        return decorated_function

    return decorator
