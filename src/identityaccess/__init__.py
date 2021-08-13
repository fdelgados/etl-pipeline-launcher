from __future__ import annotations

from enum import IntEnum


class IdentityAccessError(RuntimeError):
    def __init__(self, error: ErrorCodes, details: str = "") -> None:
        self._error = error
        self._details = details

        self.code = int(self._error.value)
        self.message = str(self._error)

        if self._details:
            self.message = "{}. {}".format(self.message, self._details)

    @property
    def error(self):
        return self._error

    @property
    def details(self):
        return self._details

    @classmethod
    def create_from_error(cls, error: IdentityAccessError) -> IdentityAccessError:
        return cls(error.error, details=error.details)


class InvalidRequestParamsException(IdentityAccessError):
    pass


class ErrorCodes(IntEnum):
    def __new__(cls, value: int, message: str):
        obj = int.__new__(cls, value)

        obj._value_ = value
        obj._message = message

        return obj

    MISSING_REQUEST_PARAMETER = 1001, "Missing request parameter"
    INVALID_REQUEST_PARAMETER = 1002, "Invalid request parameter"

    AUTHENTICATION_FAILED = 2001, "Authentication failed"
    TENANT_NOT_FOUND = 2002, "Tenant not found"
    TENANT_ACCOUNT_DEACTIVATED = 2003, "Tenant account is deactivated"
    USER_NOT_FOUND = 2004, "Incorrect username/password combination. Please try again"
    USER_DISABLED = 2005, "User is disabled"

    INVALID_ACCESS_TOKEN_TYPE = 2006, 'Access token must be of type Bearer'
    INVALID_ACCESS_TOKEN = 2007, 'Invalid access token'
    ACCESS_TOKEN_EXPIRED = 2008, 'Access token expired'
    PERMISSION_DENIED = 2009, 'Permission denied'
    TENANT_ID_MISMATCH = 2010, 'The tenant id supplied does not correspond to the tenant id of the access token'

    def __str__(self):
        return self._message
