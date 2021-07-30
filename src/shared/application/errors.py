from __future__ import annotations

from enum import IntEnum


class ApiBaseError(RuntimeError):
    def __init__(self, error: ErrorCodes, details: str = "") -> None:
        self.code = int(error.value)
        self.message = str(error)

        if details:
            self.message = "{}. {}".format(self.message, details)


class InvalidRequestParamsException(ApiBaseError):
    pass


class AccessError(ApiBaseError):
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
    TENANT_ACCOUNT_DEACTIVATE = 2003, "Tenant account deactivated"

    def __str__(self):
        return self._message
