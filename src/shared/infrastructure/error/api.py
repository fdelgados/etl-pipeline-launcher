from __future__ import annotations

from enum import IntEnum


__all__ = [
    'ErrorCodes',
    'ApiBaseError',
    'InvalidRequestParamsException',
    'MissingRequestParamsException'
]


class ApiBaseError(RuntimeError):
    def __init__(self, error: ErrorCodes, details: str = "") -> None:
        self.code = int(error.value)
        self.message = str(error)

        if details:
            self.message = "{}. {}".format(self.message, details)


class InvalidRequestParamsException(ApiBaseError):
    def __init__(self, details: str = "") -> None:
        super().__init__(ErrorCodes.INVALID_REQUEST_PARAMETER, details)


class MissingRequestParamsException(ApiBaseError):
    def __init__(self, details: str = "") -> None:
        super().__init__(ErrorCodes.MISSING_REQUEST_PARAMETER, details)


class ErrorCodes(IntEnum):
    def __new__(cls, value: int, message: str):
        obj = int.__new__(cls, value)

        obj._value_ = value
        obj._message = message

        return obj

    GENERIC_ERROR = 1000, 'Application error'
    MISSING_REQUEST_PARAMETER = 1001, 'Missing request parameter'
    INVALID_REQUEST_PARAMETER = 1002, 'Invalid request parameter'

    AUTHORIZATION_FAILED = 2001, 'Authorization failed'
    ACCESS_TOKEN_EXPIRED = 2002, 'Access token has expired. You can use the refresh token to obtain a new one'
    ACCESS_TOKEN_NOT_PROVIDED = 2003, 'Access token not provided'

    def __str__(self):
        return self._message
