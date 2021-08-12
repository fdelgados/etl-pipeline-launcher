from __future__ import annotations

from enum import IntEnum


class IdentityAccessError(RuntimeError):
    def __init__(self, error: ErrorCodes, details: str = "") -> None:
        self.code = int(error.value)
        self.message = str(error)

        if details:
            self.message = "{}. {}".format(self.message, details)


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

    def __str__(self):
        return self._message
