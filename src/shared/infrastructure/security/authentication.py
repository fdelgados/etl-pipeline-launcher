import jwt

from functools import wraps
from flask import request

from shared.infrastructure.application.settings import Settings


class AuthenticationError(RuntimeError):
    pass


class Authenticate:
    def __init__(self, argument):
        self._argument = argument

    def __call__(self, fn):
        if not callable(fn):
            raise ValueError

        @wraps(fn)
        def decorated(*args, **kwargs):

            return decorated


def authentication_required(*args, **kwargs):
    func = None
    if len(args) == 1 and callable(args[0]):
        func = args[0]

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                raise AuthenticationError("Api key not provided")

            token_type, auth_token = auth_header.split()

            if token_type != "Bearer":
                raise AuthenticationError("Api key not provided")

            try:
                payload = jwt.decode(
                    auth_token,
                    Settings.secret_key(),
                    algorithms=["HS256"]
                )

                tenant_id = str(payload.get("sub"))

                return func(tenant_id, *args, **kwargs)
            except (jwt.InvalidTokenError, ValueError) as error:
                raise AuthenticationError(str(error))

        return decorated_function

    return decorator(func) if func else decorator
